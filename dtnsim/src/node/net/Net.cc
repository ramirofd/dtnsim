#include "Net.h"
#include "App.h"

Define_Module (Net);

void Net::initialize()
{
	this->eid_ = this->getParentModule()->getIndex() + 1;

	if (hasGUI())
	{
		// Arrange graphical stuff: icon
		cDisplayString& dispStr = this->getParentModule()->getDisplayString();
		string icon_path = "device/";
		string icon = this->getParentModule()->par("icon");
		icon_path.append(icon);
		dispStr.setTagArg("i", 0, icon_path.c_str());
		// Arrange graphical stuff: circular position
		posRadius = this->getParentModule()->getVectorSize() * 250 / (2 * (3.1415));
		posAngle = 2 * (3.1415) / ((float) this->getParentModule()->getVectorSize());
		posX = posRadius * cos((eid_ - 1) * posAngle) + posRadius;
		posY = posRadius * sin((eid_ - 1) * posAngle) + posRadius;
		dispStr.setTagArg("p", 0, posX);
		dispStr.setTagArg("p", 1, posY);
	}

	// Parse contacts
	this->parseContacts(par("contactsFile"));

	// Initialize routing
	string routeString = par("routing");
	if (routeString.compare("direct") == 0)
		routing = new RoutingDirect();
	if (routeString.compare("cgrModel") == 0)
		routing = new RoutingCgrModel();
	if (routeString.compare("cgrIon350") == 0)
		routing = new RoutingCgrIon350();
	routing->setLocalNode(eid_);
	routing->setQueue(&bundlesQueue_);
	routing->setContactPlan(&contactPlan_);

	// Initialize faults
	if (this->getParentModule()->par("enableFaults").boolValue() == true)
	{
		meanTTF = this->getParentModule()->par("meanTTF").doubleValue();
		meanTTR = this->getParentModule()->par("meanTTR").doubleValue();

		cMessage *faultMsg = new ContactMsg("fault", FAULT_START_TIMER);
		//faultMsg->setSchedulingPriority(4);
		scheduleAt(exponential(meanTTF), faultMsg);
	}
}

void Net::handleMessage(cMessage * msg)
{
	if (msg->getKind() == BUNDLE)
	{
		Bundle* bundle = check_and_cast<Bundle *>(msg);

		bubble("dispatching bundle");
		dispatchBundle(bundle);
	}
	else if (msg->getKind() == FAULT_START_TIMER)
	{
		if (hasGUI())
		{
			// Visualize fault start
			cDisplayString& dispStr = this->getParentModule()->getDisplayString();
			string faultColor = "red";
			dispStr.setTagArg("i", 1, faultColor.c_str());
			dispStr.setTagArg("i2", 0, "status/stop");
		}

		// Schedule fault recovery
		msg->setKind(FAULT_END_TIMER);
		scheduleAt(simTime() + exponential(meanTTR), msg);
	}
	else if (msg->getKind() == FAULT_END_TIMER)
	{
		if (hasGUI())
		{
			// Visualize fault end
			cDisplayString& dispStr = this->getParentModule()->getDisplayString();
			dispStr.setTagArg("i", 1, "");
			dispStr.setTagArg("i2", 0, "");
		}

		// Schedule next fault
		msg->setKind(FAULT_START_TIMER);
		scheduleAt(simTime() + exponential(meanTTF), msg);
	}
	else if (msg->getKind() == CONTACT_START_TIMER)
	{
		// Schedule end of contact
		ContactMsg* contactMsg = check_and_cast<ContactMsg *>(msg);
		contactMsg->setKind(CONTACT_END_TIMER);
		contactMsg->setName("ContactEnd");
		contactMsg->setSchedulingPriority(3);
		scheduleAt(simTime() + contactMsg->getDuration(), contactMsg);

		// Schedule start of transmission
		FreeChannelMsg* freeChannelMsg = new FreeChannelMsg("FreeChannelMsg", FREE_CHANNEL);
		freeChannelMsg->setSchedulingPriority(1);
		freeChannelMsg->setNeighborEid(contactMsg->getDestinationEid());
		freeChannelMsg->setContactId(contactMsg->getId());
		freeChannelMsgs_[contactMsg->getId()] = freeChannelMsg;
		scheduleAt(simTime(), freeChannelMsg);

		if (hasGUI())
		{
			// Visualize contact line
			cCanvas *canvas = getParentModule()->getParentModule()->getCanvas();
			string lineName = "line";
			lineName.append(to_string(contactMsg->getDestinationEid()));
			cLineFigure *line = new cLineFigure(lineName.c_str());
			line->setStart(cFigure::Point(posX, posY));
			line->setEnd(cFigure::Point(posRadius * cos((contactMsg->getDestinationEid() - 1) * posAngle) + posRadius, posRadius * sin((contactMsg->getDestinationEid() - 1) * posAngle) + posRadius));
			line->setLineWidth(2);
			line->setEndArrowhead(cFigure::ARROW_BARBED);
			lines.push_back(line);
			canvas->addFigure(line);
		}

	}
	else if (msg->getKind() == CONTACT_END_TIMER)
	{
		ContactMsg* contactMsg = check_and_cast<ContactMsg *>(msg);

		if (hasGUI())
		{
			// Visualize contact line end
			cCanvas *canvas = getParentModule()->getParentModule()->getCanvas();
			string lineName = "line";
			lineName.append(to_string(contactMsg->getDestinationEid()));
			canvas->removeFigure(canvas->findFigureRecursively(lineName.c_str()));
		}

		int contactId = contactMsg->getId();
		cancelAndDelete(freeChannelMsgs_[contactId]);
		delete contactMsg;
	}
	else if (msg->getKind() == FREE_CHANNEL)
	{
		FreeChannelMsg* freeChannelMsg = check_and_cast<FreeChannelMsg *>(msg);
		int neighborEid = freeChannelMsg->getNeighborEid();
		int contactId = freeChannelMsg->getContactId();

		// save freeChannelMsg to cancel event if necessary
		freeChannelMsgs_[freeChannelMsg->getContactId()] = freeChannelMsg;

		map<int, queue<Bundle *> >::iterator it = bundlesQueue_.find(contactId);

		// if there are messages in the queue for this contact
		if (it != bundlesQueue_.end())
		{
			// TODO: Need to stop from transmitting if this node
			// or the next hop is with failure.
			// transmit bundle and get transmissionDuration
			double transmissionDuration = transmitBundle(neighborEid, contactId);

			// simulate bundle transmission duration by scheduling freeChannelMsg
			scheduleAt(simTime() + transmissionDuration, freeChannelMsg);
		}
		// if there aren't messages for this contact, delete freeChannelMsg to stop trying to send bundles through this contact
		else
		{
			// TODO: this needs to be changed, if new bundles are sent
			// from the App they will not be transmitted after this.
			freeChannelMsgs_[freeChannelMsg->getContactId()] = nullptr;
			delete freeChannelMsg;
		}
	}
}

void Net::dispatchBundle(Bundle *bundle)
{
	int destinationEid = bundle->getDestinationEid();
	int ownEid = this->eid_;

	// if this node is the destination, send the bundle to Application Module
	if (ownEid == destinationEid)
	{
		send(bundle, "gateToApp$o");
	}
	// else, route and enqueue bundle
	else
	{
		routing->routeBundle(bundle, simTime().dbl());
	}
}

double Net::transmitBundle(int neighborEid, int contactId)
{
	double transmissionDuration = 0.0;

	map<int, queue<Bundle *> >::iterator it = bundlesQueue_.find(contactId);

	// if there is a bundlesQueue for the contact
	if (it != bundlesQueue_.end())
	{
		queue<Bundle *> bundlesToTx = it->second;

		// if the queue is not empty
		// send one bundle to Mac Module
		// and erase bundle pointer from the queue
		if (!bundlesToTx.empty())
		{
			Bundle* bundle = bundlesToTx.front();
			double dataRate = this->contactPlan_.getContactById(contactId)->getDataRate();
			transmissionDuration = (double) bundle->getBitLength() / dataRate;

			// Set things that changes on each hop:
			bundle->setSenderEid(eid_);
			bundle->setDlvConfidence(0);
			bundle->setXmitCopiesCount(0);

			send(bundle, "gateToMac$o");
			bundlesToTx.pop();

			if (!bundlesToTx.empty())
			{
				bundlesQueue_[contactId] = bundlesToTx;
			}
			else
			{
				bundlesQueue_.erase(contactId);
			}
		}
	}

	return transmissionDuration;
}

void Net::parseContacts(string fileName)
{
	int id = 1;
	double start = 0.0;
	double end = 0.0;
	int sourceEid = 0;
	int destinationEid = 0;
	double dataRate = 0.0;

	string aux = "#";
	string a;
	string command;
	ifstream file;
	file.open(fileName.c_str());

	if (!file.is_open())
		throw cException(("Error: wrong path to contacts file " + string(fileName)).c_str());

	while (true)
	{
		if (aux.empty())
			getline(file, aux, '\n');
		else if (aux.at(0) == '#')
			getline(file, aux, '\n');
		else
			break;
	}

	stringstream ss(aux);
	ss >> a >> command >> start >> end >> sourceEid >> destinationEid >> dataRate;

	do
	{
		if ((command.compare("contact") == 0))
		{
			contactPlan_.addContact(id, start, end, sourceEid, destinationEid, dataRate, (float) 1.0);
			if (this->eid_ == sourceEid)
			{
				ContactMsg *contactMsg = new ContactMsg("contactStart", CONTACT_START_TIMER);
				contactMsg->setSchedulingPriority(4);
				contactMsg->setId(id);
				contactMsg->setStart(start);
				contactMsg->setEnd(end);
				contactMsg->setDuration(end - start);
				contactMsg->setSourceEid(sourceEid);
				contactMsg->setDestinationEid(destinationEid);
				contactMsg->setDataRate(dataRate);
				scheduleAt(start, contactMsg);
			}
			id++;
		}
	} while (file >> a >> command >> start >> end >> sourceEid >> destinationEid >> dataRate);

	file.close();
}

void Net::finish()
{
	//delete enqueued bundles that could not be delivered
	map<int, queue<Bundle *> >::iterator it1 = bundlesQueue_.begin();
	map<int, queue<Bundle *> >::iterator it2 = bundlesQueue_.end();
	while (it1 != it2)
	{
		queue<Bundle *> bundles = it1->second;

		while (!bundles.empty())
		{
			delete (bundles.front());
			bundles.pop();
		}
		bundlesQueue_.erase(it1++);
	}

	// Remove and delete visualization lines
	cCanvas *canvas = getParentModule()->getParentModule()->getCanvas();
	for (vector<cLineFigure *>::iterator it = lines.begin(); it != lines.end(); ++it)
	{
		if (canvas->findFigure((*it)) != -1)
			canvas->removeFigure((*it));
		delete (*it);
	}
}

Net::Net()
{

}

Net::~Net()
{

}

