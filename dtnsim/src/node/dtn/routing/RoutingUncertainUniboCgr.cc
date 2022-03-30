/*
 * RoutingUncertainUniboCgr.cc
 *
 *  Created on: Jan 16, 2022
 *      Author: simon
 */

#include "RoutingUncertainUniboCgr.h"
#include <src/node/dtn/Dtn.h>
#include "src/node/dtn/routing/unibocgr/core/cgr/cgr_phases.h"
#include "src/node/dtn/routing/unibocgr/core/contact_plan/contactPlan.h"
#include "src/node/dtn/routing/unibocgr/core/contact_plan/nodes/nodes.h"
#include "src/node/dtn/routing/unibocgr/core/library/list/list.h"
#include "src/node/dtn/routing/unibocgr/core/bundles/bundles.h"

static SdrModel *sdrUnibo;
static json brufFunction;
static int currDest;
static int numOfTs;
static int tsDuration;
bool useUncertainMode;
static map<int, vector<int>> tsStartTimes;

int getTotalEVC(vector<int> sizes);
double getNodeFutureDeliveryProbability(int carrierEid, int ts);
int getTsForStartOrCurrentTime(int startOrCurrent);
int getTsForEndTime(int end);
int findMaxTs();
void updateStartTimes(vector<Contact> *contacts);
vector<int> getTsForContact(Contact *contact);

RoutingUncertainUniboCgr::RoutingUncertainUniboCgr(int eid, SdrModel *sdr, ContactPlan *contactPlan, cModule *dtn, MetricCollector *metricCollector, int tsIntervalDuration, bool useUncertainty, int repetition, int numOfNodes) :
		RoutingOpportunistic(eid, sdr, contactPlan, dtn, metricCollector)
{
	sdrUnibo = this->sdr_;
	tsDuration = tsIntervalDuration;
	useUncertainMode = useUncertainty;
	if (useUncertainty)
	{
		this->metricCollector_->setAlgorithm("OCGR-UCoP");
	}
	else
	{
		this->metricCollector_->setAlgorithm("OCGR");
	}

	this->opportunistic = this->metricCollector_->getMode() == 1;

	if (eid == 0)
	{
		return;
	}

	if (repetition > 0 && useUncertainty)
	{
		for (int j = 1; j <= numOfNodes; j++)
		{
			currDest = j;
			string pathToFiles = "sharedFolder/";
			{
				string filePath = pathToFiles + to_string(j) + ".txt";
				ifstream file(filePath);

				if (file.good())
				{
					this->nodeBrufFunction_[j] = json::parse(file);
				}
				else
				{
					//cout << "An error happened trying to read the routing decisions for file " + filePath;
				}
			}
			updateStartTimes(this->contactPlan_->getContacts());

			this->tsStartTimes_[currDest] = tsStartTimes[currDest];
		}
	}

	int result = this->initializeUniboCGR(0);

	cout << "UniboCGR initialized with" << result << endl;

}

RoutingUncertainUniboCgr::~RoutingUncertainUniboCgr()
{

	// TODO Auto-generated destructor stub
}

void RoutingUncertainUniboCgr::routeAndQueueBundle(BundlePkt *bundle, double simTime)
{
	if (opportunistic)
	{
		this->contactPlan_->deleteOldContacts();
	}

	currDest = bundle->getDestinationEid();
	tsStartTimes[currDest] = this->tsStartTimes_[currDest];
	numOfTs = this->maxTs_[currDest];
	//this->modifyUniboContactPlan();

	List cgrRoutes = NULL;
	ListElt *elt;
	if (bundle->getSenderEid() == 0)
	{
		this->metricCollector_->updateStartedBundles(eid_, bundle->getBundleId(), bundle->getSourceEid(), bundle->getDestinationEid(), simTime);
	}
	int numberOfRoutes = 1;
	currDest = bundle->getDestinationEid();
	if (this->multiHops.find(bundle->getBundleId()) != this->multiHops.end())
	{
		this->enqueueBundle(bundle, simTime, NULL);
		return;
	}
	if (useUncertainMode && this->nodeBrufFunction_.find(currDest) == this->nodeBrufFunction_.end())
	{
		this->callToPython();
		brufFunction = this->nodeBrufFunction_[currDest];
	}
	else if (useUncertainMode && this->lastTimeUpdated_[bundle->getDestinationEid()] < this->contactPlan_->getLastEditTime().dbl())
	{
		this->callToPython();
		brufFunction = this->nodeBrufFunction_[currDest];
	}
	else
	{
		brufFunction = this->nodeBrufFunction_[currDest];
	}

	int result = this->callUniboCGR(simTime, bundle, &cgrRoutes);
	//routes were found!
	if (result >= 0 && cgrRoutes != NULL)
	{
		//enqueue the bundle to every route
		for (elt = cgrRoutes->first; elt != NULL && result >= 0; elt = elt->next)
		{

			if (elt->data != NULL)
			{

				Route *route = (Route*) elt->data;

				if (route->neighbor == bundle->getSenderEid())
				{
					bundle->setNextHopEid(0);
					this->sdr_->enqueueBundleToContact(bundle, 0);
					break;
				}

				if (numberOfRoutes == 1)
				{

					bundle->setDlvConfidence(bundle->getDlvConfidence() + (1 - (1 - route->arrivalConfidence) * (1 - bundle->getDlvConfidence())));

					if (bundle->getDlvConfidence() >= 1.0)
					{
						bundle->setDlvConfidence(1.0);
					}

					this->enqueueBundle(bundle, simTime, route);

					if (bundle->getDlvConfidence() >= 0.8)
					{
						break;
					}

					numberOfRoutes++;

				}
				else
				{
					BundlePkt *bundleCopy = bundle->dup();

					bundleCopy->setDlvConfidence(bundleCopy->getDlvConfidence() + (1 - (1 - route->arrivalConfidence) * (1 - bundleCopy->getDlvConfidence())));

					if (bundleCopy->getDlvConfidence() >= 1.0)
					{
						bundleCopy->setDlvConfidence(1.0);
					}

					this->enqueueBundle(bundleCopy, simTime, route);

					if (bundleCopy->getDlvConfidence() >= 0.8)
					{
						break;
					}

					numberOfRoutes++;
				}

			}
			else
			{
				break;
			}

		}
	}
	else
	{
		bundle->setNextHopEid(0);
		this->sdr_->enqueueBundleToContact(bundle, 0);
	}
}

void RoutingUncertainUniboCgr::contactFailure(int contactId)
{
	while (sdr_->isBundleForContact(contactId))
	{
		BundlePkt *bundle = sdr_->getNextBundleForContact(contactId);
		sdr_->popNextBundleForContact(contactId);
		this->routeAndQueueBundle(bundle, simTime().dbl());
	}

}

void RoutingUncertainUniboCgr::notifyAboutMultiHop(vector<int>hops, long bundleId)
{
	this->multiHops[bundleId] = hops;
}

void RoutingUncertainUniboCgr::notifyAboutRouting(json jsonFunction, int destination)
{
	this->nodeBrufFunction_[destination] = jsonFunction;
	this->lastTimeUpdated_[destination] = simTime().dbl();
	this->maxTs_[destination] = numOfTs;
	this->tsStartTimes_[destination] = tsStartTimes[destination];
}

vector<int> RoutingUncertainUniboCgr::hasMultiHop(Route *route)
{
	int ts = getTsForStartOrCurrentTime(route->fromTime);
	vector<int> hopsWithinTs;

	for (ListElt *elt = route->hops->first; elt != NULL; elt = elt->next)
	{
		UniboContact *currHop = (UniboContact*) elt->data;
		if (getTsForStartOrCurrentTime(currHop->fromTime) == ts)
		{
			hopsWithinTs.push_back(currHop->toNode);
		}
		else
		{
			break;
		}
	}

	return hopsWithinTs;
}

void RoutingUncertainUniboCgr::enqueueBundle(BundlePkt *bundle, double simTime, Route *route)
{


	//multi hop!!
	if (route == NULL)
	{
		int destination = this->multiHops[bundle->getBundleId()].front();

		Dtn *dtn = check_and_cast<Dtn*>(dtn_->getParentModule()->getParentModule()->getSubmodule("node", destination)->getSubmodule("dtn"));

		RoutingUncertainUniboCgr *other = check_and_cast<RoutingUncertainUniboCgr*>(dtn->getRouting());
		Contact* contactDtnSim = this->contactPlan_->getContactBySrcDstStart(this->eid_, destination, simTime);

		if (contactDtnSim == NULL)
		{
			bundle->setNextHopEid(0);
			this->sdr_->enqueueBundleToContact(bundle, 0);
			return;
		}
		int id;

		if (contactDtnSim->isDiscovered() || contactDtnSim->isPredicted())
		{
			id = dtn->checkExistenceOfContact(this->eid_, destination, simTime);
		}
		else
		{

		id = contactDtnSim->getId();
		}

		if (id == 0)
		{
				bundle->setNextHopEid(0);
				this->sdr_->enqueueBundleToContact(bundle, 0);
				this->bundleReroutable[bundle->getBundleId()].push(simTime);
				this->multiHops.erase(bundle->getBundleId());
				return;
		}

		this->multiHops[bundle->getBundleId()].erase(this->multiHops[bundle->getBundleId()].begin());

		if (this->multiHops[bundle->getBundleId()].size() > 0)
		{
			other->notifyAboutMultiHop(this->multiHops[bundle->getBundleId()], bundle->getBundleId());
		}

		this->multiHops.erase(bundle->getBundleId());
		this->metricCollector_->updateSentBundles(eid_, destination, simTime, bundle->getBundleId());
		other->notifyAboutRouting(this->nodeBrufFunction_[currDest], currDest);
		bundle->setNextHopEid(destination);
		this->sdr_->enqueueBundleToContact(bundle, id);
		return;

	}
	int sourceEid = this->eid_;
	int destinationEid = route->neighbor;
	double start = route->fromTime;

	vector<int> hops;

	if (useUncertainMode)
	{
		hops = this->hasMultiHop(route);
	}

	if (hops.size() > 1) //multi hop!
	{

		int destination = hops[0];

		Dtn *dtn = check_and_cast<Dtn*>(dtn_->getParentModule()->getParentModule()->getSubmodule("node", destination)->getSubmodule("dtn"));

		RoutingUncertainUniboCgr *other = check_and_cast<RoutingUncertainUniboCgr*>(dtn->getRouting());
		Contact* contactDtnSim = this->contactPlan_->getContactBySrcDstStart(this->eid_, destination, start);

		if (contactDtnSim == NULL)
		{
			bundle->setNextHopEid(0);
			this->sdr_->enqueueBundleToContact(bundle, 0);
			return;
		}
		int id;

		if (contactDtnSim->isDiscovered() || contactDtnSim->isPredicted())
		{
			id = dtn->checkExistenceOfContact(this->eid_, destination, simTime);
		}
		else
		{

		id = contactDtnSim->getId();
		}

		if (id == 0)
		{
			bundle->setNextHopEid(0);
			this->sdr_->enqueueBundleToContact(bundle, 0);
			this->bundleReroutable[bundle->getBundleId()].push(start);
			return;
		}

		hops.erase(hops.begin());

		if (hops.size() > 0)
		{
			other->notifyAboutMultiHop(hops, bundle->getBundleId());
		}
		other->notifyAboutRouting(this->nodeBrufFunction_[currDest], currDest);
		this->metricCollector_->updateSentBundles(eid_, destination, start, bundle->getBundleId());
		bundle->setNextHopEid(destination);
		this->sdr_->enqueueBundleToContact(bundle, id);
		return;
	}



	Contact *contactDtnSim = this->contactPlan_->getContactBySrcDstStart(sourceEid, destinationEid, start);

	Dtn *dtn = check_and_cast<Dtn*>(dtn_->getParentModule()->getParentModule()->getSubmodule("node", destinationEid)->getSubmodule("dtn"));

	RoutingUncertainUniboCgr *other = check_and_cast<RoutingUncertainUniboCgr*>(dtn->getRouting());

	if (contactDtnSim == NULL)
	{
		bundle->setNextHopEid(0);
		this->sdr_->enqueueBundleToContact(bundle, 0);
		return;
	}

	int contactId;
	int id = contactDtnSim->getId();

	if (contactDtnSim->isPredicted() || contactDtnSim->isDiscovered()) //check if a predicted neighbor is actually happening
	{

		contactId = dtn->checkExistenceOfContact(sourceEid, destinationEid, start);

		if (contactId == 0)
		{
			bundle->setNextHopEid(0);
			this->sdr_->enqueueBundleToContact(bundle, 0);
			this->bundleReroutable[bundle->getBundleId()].push(start);
			return;
		}
		this->metricCollector_->updateSentBundles(eid_, destinationEid, start, bundle->getBundleId());
		bundle->setNextHopEid(this->contactPlan_->getContactById(id)->getDestinationEid());
		if (contactDtnSim->getStart() < simTime)
		{
			other->notifyAboutRouting(this->nodeBrufFunction_[bundle->getDestinationEid()], bundle->getDestinationEid());
		}
		this->sdr_->enqueueBundleToContact(bundle, contactId);
		return;
	}

	if (id != 0)
	{
		bundle->setNextHopEid(this->contactPlan_->getContactById(id)->getDestinationEid());
	}
	this->metricCollector_->updateSentBundles(eid_, destinationEid, start, bundle->getBundleId());

	if (contactDtnSim->getStart() < simTime)
	{
		other->notifyAboutRouting(this->nodeBrufFunction_[bundle->getDestinationEid()], bundle->getDestinationEid());
	}

	this->sdr_->enqueueBundleToContact(bundle, id);
}

int RoutingUncertainUniboCgr::convertBundlePktToCgrBundle(time_t time, BundlePkt *bundle, CgrBundle *cgrBundle)
{
	if (bundle == NULL || cgrBundle == NULL)
	{
		return -1;
	}

	cgrBundle->id.source_node = bundle->getSourceEid();
	cgrBundle->id.creation_timestamp = bundle->getCreationTimestamp().dbl() - this->referenceTime_;
	cgrBundle->id.sequence_number = bundle->getBundleId();
	cgrBundle->id.fragment_length = 0;
	cgrBundle->id.fragment_offset = 0;
	cgrBundle->size = bundle->getByteLength();
	cgrBundle->dlvConfidence = bundle->getDlvConfidence();
	cgrBundle->evc = computeBundleEVC(bundle->getByteLength());
	if (bundle->getCritical())
	{
		cgrBundle->priority_level = Expedited;
	}
	else
	{
		cgrBundle->priority_level = Normal;
	}
	cgrBundle->sender_node = bundle->getSenderEid();
	cgrBundle->regionNbr = this->defaultRegionNbr_;
	cgrBundle->terminus_node = bundle->getDestinationEid();
	cgrBundle->expiration_time = bundle->getTtl().dbl() + cgrBundle->id.creation_timestamp;

	return 0;

}

int RoutingUncertainUniboCgr::addContactToSap(Contact *contact)
{
	int result = addContact(this->defaultRegionNbr_, contact->getSourceEid(), contact->getDestinationEid(), contact->getStart(), contact->getEnd(), contact->getDataRate(), contact->getConfidence(), 0, NULL,
			contact->getFailureProbability(), false);

	if (result <= 0)
	{
		return result;
	}

	result = addRange(contact->getSourceEid(), contact->getDestinationEid(), contact->getStart(), contact->getEnd(), contact->getRange());

	return result;
}



int RoutingUncertainUniboCgr::removeContactFromSap(Contact *contact)
{
	int result = 0;

	result = removeContact(this->defaultRegionNbr_, contact->getSourceEid(), contact->getDestinationEid(), NULL);

	if (result <= 0)
	{
		return result;
	}

	result = removeRange(contact->getSourceEid(), contact->getDestinationEid(), NULL);

	return result;
}

void RoutingUncertainUniboCgr::updateContactPlan(Contact *c)
{
	// this->populateContactPlan(); return; //(much) slower, but working
	this->restoreSAPvalues();
	ContactPlanSAP cpSAP = get_contact_plan_sap(NULL);

	if (c == NULL)
	{
		for (int i = this->lastId_ + 1; i <= this->contactPlan_->getHighestId(); i++)
		{
			this->addContactToSap(this->contactPlan_->getContactById(i));
		}
	}
	else
	{
		this->removeContactFromSap(c);
	}

	cpSAP.contactPlanEditTime.tv_sec = simTime().dbl();
	cpSAP.contactPlanEditTime.tv_usec = simTime().inUnit(SIMTIME_US);
	set_time_contact_plan_updated(cpSAP.contactPlanEditTime.tv_sec, cpSAP.contactPlanEditTime.tv_usec);

	get_contact_plan_sap(&cpSAP); //save

	this->saveSAPs();

	this->lastId_ = this->contactPlan_->getHighestId();

}

int RoutingUncertainUniboCgr::populateContactPlan()
{
	this->restoreSAPvalues();
	int result = 1;
	int addResult = 1;
	ContactPlanSAP cpSAP = get_contact_plan_sap(NULL);
	reset_contact_plan();

	vector<Contact> *contacts = this->contactPlan_->getContacts();

	for (size_t i = 0; i < (*contacts).size(); i++)
	{
		addResult = this->addContactToSap(&((*contacts).at(i)));
		cout << "Contact from" << (*contacts).at(i).getSourceEid() << "with" << addResult << endl;
		if (addResult <= 0)
		{ //contact was not added successfully
			result = 0;
		}
	}

	//update last edit time
	cpSAP.contactPlanEditTime.tv_sec = simTime().dbl();
	cpSAP.contactPlanEditTime.tv_usec = simTime().inUnit(SIMTIME_US);
	set_time_contact_plan_updated(cpSAP.contactPlanEditTime.tv_sec, cpSAP.contactPlanEditTime.tv_usec);

	get_contact_plan_sap(&cpSAP); //save

	this->saveSAPs();

	this->lastId_ = contacts->size();

	return result;

}

int RoutingUncertainUniboCgr::initializeUniboCGR(time_t time)
{
	int result = 1;
	this->initializeSAPValues();
	this->restoreSAPvalues();

	if (!this->initialised_)
	{
		this->excludedNeighbors_ = list_create(NULL, NULL, NULL, free);
		this->cgrBundle_ = bundle_create();

		if (this->cgrBundle_ != NULL && this->excludedNeighbors_ != NULL)
		{
			result = initialize_cgr(0, this->eid_, true);

			if (result == 1)
			{
				this->initialised_ = true;
				this->referenceTime_ = time;
				this->saveSAPs();

				if (this->populateContactPlan() <= 0)
				{
					result = -2;
				}

				this->saveSAPs();
			}
		}
		else
		{ //something went wrong
			free_list(this->excludedNeighbors_);
			bundle_destroy(this->cgrBundle_);
			this->excludedNeighbors_ = NULL;
			this->cgrBundle_ = NULL;
			result = -2;
		}
	}

	return result;
}

int RoutingUncertainUniboCgr::callUniboCGR(time_t time, BundlePkt *bundle, List *cgrRoutes)
{
	int result;
	this->restoreSAPvalues();
	sdrUnibo = this->sdr_;
	this->metricCollector_->updateCGRCalls(this->eid_);

	if (this->initialised_ && bundle != NULL)
	{
		result = this->convertBundlePktToCgrBundle(time, bundle, this->cgrBundle_);

		if (result >= 0)
		{
			auto start = high_resolution_clock::now();
			result = getBestRoutes(time - this->referenceTime_, this->cgrBundle_, this->excludedNeighbors_, cgrRoutes);
			auto stop = high_resolution_clock::now();
			auto duration = duration_cast<seconds>(stop - start);
			this->metricCollector_->updateCGRComputationTime(duration.count());
			cout << "Result of Best routes:" << result << endl;
			if (result > 0 && cgrRoutes != NULL)
			{
				result = 0;

			}
			else
			{
				result = -3;
			}
		}
		else
		{
			result = -2;
		}

	}
	else
	{
		result = -1;
	}
	reset_bundle(this->cgrBundle_);
	this->saveSAPs();
	return result;
}

void RoutingUncertainUniboCgr::initializeSAPValues()
{
	//set important values in certains SAPs to ensure correct initialization
	this->rangeGraphSAP.ranges = NULL;
	this->neighborsSAP.local_node_neighbors = NULL;
	this->neighborsSAP.neighbors_list_builded = 0;
	this->neighborsSAP.timeNeighborToRemove = -1;
	this->contactGraphSAP.contacts = NULL;
	this->contactPlanSAP.initialized = 0;
	this->contactPlanSAP.contactsGraph = 0;
	this->contactPlanSAP.nodes = 0;
	this->contactPlanSAP.rangesGraph = 0;
	this->contactPlanSAP.contactPlanEditTime.tv_sec = -1;
	this->contactPlanSAP.contactPlanEditTime.tv_sec = -1;
	this->phaseOneSAP.excludedNeighbors = NULL;
	this->phaseTwoSAP.routes = NULL;
	this->phaseTwoSAP.subset = NULL;
	this->phaseTwoSAP.suppressedNeighbors = NULL;
}

void RoutingUncertainUniboCgr::saveSAPs()
{
	//update local SAPs
	this->contactGraphSAP = *get_contact_graph_sap(NULL);
	this->contactPlanSAP = get_contact_plan_sap(NULL);
	this->neighborsSAP = *get_neighbors_sap(NULL);
	this->rangeGraphSAP = *get_range_graph_sap(NULL);
	this->nodesRbt = *get_node_graph(NULL);
	this->uniboCgrSAP = get_unibo_cgr_sap(NULL);
	this->uniboCgrCurrentCallSAP = *get_current_call_sap(NULL);
	this->phaseOneSAP = *get_phase_one_sap(NULL);
	this->phaseTwoSAP = *get_phase_two_sap(NULL);
}

void RoutingUncertainUniboCgr::restoreSAPvalues()
{
	//overwrite all SAPs with the addresses of the local SAPs
	get_contact_graph_sap(&this->contactGraphSAP);
	get_contact_plan_sap(&this->contactPlanSAP);
	get_neighbors_sap(&this->neighborsSAP);
	get_range_graph_sap(&this->rangeGraphSAP);
	get_node_graph(&this->nodesRbt);
	get_unibo_cgr_sap(&this->uniboCgrSAP);
	get_current_call_sap(&this->uniboCgrCurrentCallSAP);
	get_phase_one_sap(&this->phaseOneSAP);
	get_phase_two_sap(&this->phaseTwoSAP);
}

void RoutingUncertainUniboCgr::successfulBundleForwarded(long bundleId, Contact *contact, bool sentToDestination)
{
	if (sentToDestination)
	{
		this->deliveredBundles_.push_back(bundleId);
	}
}

bool RoutingUncertainUniboCgr::isDeliveredBundle(long bundleId)
{
	for (size_t i = 0; i < this->deliveredBundles_.size(); i++)
	{
		if (bundleId == this->deliveredBundles_[i])
		{
			return true;
		}
	}

	return false;
}

bool RoutingUncertainUniboCgr::msgToMeArrive(BundlePkt *bundle)
{
	if (!this->isDeliveredBundle(bundle->getBundleId()))
	{

		this->deliveredBundles_.push_back(bundle->getBundleId());
		this->metricCollector_->updateReceivedBundles(this->eid_, bundle->getBundleId(), simTime().dbl());
		return true;
	}

	return false;
}

void RoutingUncertainUniboCgr::contactStart(Contact *c)
{
	vector<BundlePkt*> toBeRerouted;

	while (this->sdr_->isBundleForContact(0))
	{
		BundlePkt *bundle = this->sdr_->getNextBundleForContact(0);
		toBeRerouted.push_back(bundle);
		this->sdr_->popNextBundleForContact(0);
	}
	vector<BundlePkt*> routeLater;
	//try out whether a new route exists for a newly discovered contact
	for (size_t i = 0; i < toBeRerouted.size(); i++)
	{
		BundlePkt *bundle = toBeRerouted.at(i);
		if (this->bundleReroutable.find(bundle->getBundleId()) == this->bundleReroutable.end())
		{
			if (c->isDiscovered())
			{
				this->routeAndQueueBundle(bundle, simTime().dbl());
			}
			else
			{

				routeLater.push_back(bundle);
			}
		}
		else
		{
			bool reRoutable = this->bundleReroutable[bundle->getBundleId()].front() < simTime().dbl();

			if (reRoutable)
			{
				this->routeAndQueueBundle(bundle, simTime().dbl());
				this->bundleReroutable[bundle->getBundleId()].pop();
			}
			else
			{
				routeLater.push_back(bundle);
			}
		}

	}

	for (auto it = routeLater.begin(); it != routeLater.end(); it++)
	{
		this->sdr_->enqueueBundleToContact((*it), 0);
	}

	//check whether some bundles were already received at their respective destinations!
	RoutingUncertainUniboCgr *other = check_and_cast<RoutingUncertainUniboCgr*>(check_and_cast<Dtn*>(dtn_->getParentModule()->getParentModule()->getSubmodule("node", c->getDestinationEid())->getSubmodule("dtn"))->getRouting());

	list<BundlePkt*> nonReceived;
	while (sdr_->isBundleForContact(c->getId()))
	{
		BundlePkt *bundle = sdr_->getNextBundleForContact(c->getId());
		sdr_->popNextBundleForContact(c->getId());
		if (!other->isDeliveredBundle(bundle->getBundleId()))
		{
			nonReceived.push_back(bundle);
		}
		else
		{
			delete bundle;
		}
	}

	for (list<BundlePkt*>::iterator it = nonReceived.begin(); it != nonReceived.end(); ++it)
	{
		sdr_->enqueueBundleToContact(*it, c->getId());
		other->notifyAboutRouting(this->nodeBrufFunction_[(*it)->getDestinationEid()], (*it)->getDestinationEid());
	}
}

void RoutingUncertainUniboCgr::contactEnd(Contact *c)
{
	while (sdr_->isBundleForContact(c->getId()))
	{
		BundlePkt *bundle = sdr_->getNextBundleForContact(c->getId());
		sdr_->popNextBundleForContact(c->getId());
		routeAndQueueBundle(bundle, simTime().dbl());
	}
}

void RoutingUncertainUniboCgr::callToPython()
{
	char currDirectory[128];
	getcwd(currDirectory, 128); //save current directory

	chdir("../../../");

	updateStartTimes(this->contactPlan_->getContacts());

	this->convertContactPlanIntoNet();
	this->createSourceDestFile();

	auto start = high_resolution_clock::now();
	system("./run_cgrbruf.py"); //"venv/bin/python run_bruf.py"
	auto stop = high_resolution_clock::now();
	auto duration = duration_cast<seconds>(stop - start);
	this->metricCollector_->updateRUCoPComputationTime(duration.count());

	this->readJsonFromFile();

	system("rm -r working_dir");
	system("rm net.py");
	system("rm sourcetarget.txt");

	this->lastTimeUpdated_[currDest] = simTime().dbl();
	this->metricCollector_->updateRUCoPCalls(this->eid_);

	this->tsStartTimes_[currDest] = tsStartTimes[currDest];
	brufFunction = this->nodeBrufFunction_[currDest];

	chdir(currDirectory); //return to current directory

	ofstream jsonFile("sharedFolder/" + to_string(currDest) + ".txt");
	jsonFile << this->nodeBrufFunction_[currDest] << endl;

}

void RoutingUncertainUniboCgr::convertContactPlanIntoNet()
{
	ofstream networkFile("net.py");
	int numOfNodes = this->dtn_->getParentModule()->getParentModule()->par("nodesNumber");

	networkFile << "NUM_OF_NODES = " << to_string(numOfNodes) << endl;

	string contactString = "CONTACTS = [";
	vector<Contact> *contacts = this->contactPlan_->getContacts();

	for (size_t i = 0; i < contacts->size(); i++)
	{
		int source = contacts->at(i).getSourceEid() - 1;
		int destination = contacts->at(i).getDestinationEid() - 1;
		vector<int> tsValues = getTsForContact(&contacts->at(i));
		double pf = contacts->at(i).getFailureProbability();
		for (size_t i = 0; i < tsValues.size(); i++)
		{
			contactString = contactString + "{'from': " + to_string(source) + ", ";
			contactString = contactString + "'to': " + to_string(destination) + ", ";
			contactString = contactString + "'ts': " + to_string(tsValues.at(i)) + ", ";
			contactString = contactString + "'pf': " + to_string(pf) + "}, ";
		}
	}

	contactString = contactString + "]";

	networkFile << contactString << endl;

	networkFile.close();
}


void RoutingUncertainUniboCgr::createSourceDestFile()
{
	ofstream sourceDestFile("sourcetarget.txt");
	sourceDestFile << this->eid_ - 1 << "," << currDest - 1 << endl;
	sourceDestFile.close();
}

int getTsForStartOrCurrentTime(int startOrCurrent)
{

	for (size_t i = 0; i < tsStartTimes[currDest].size() - 1; i++)
	{
		if (startOrCurrent == tsStartTimes[currDest].at(i) || startOrCurrent < tsStartTimes[currDest].at(i + 1))
		{
			return i;
		}
	}

}

int getTsForEndTime(int end)
{

	for (size_t i = 1; i < tsStartTimes[currDest].size(); i++)
	{
		if (end == tsStartTimes[currDest].at(i))
		{
			return i - 1;
		}
	}

}

void RoutingUncertainUniboCgr::readJsonFromFile()
{
	string filename = "working_dir/CGR-UCOP/routing_files/decisions.json";
	ifstream infile(filename);

	if (infile.good())
	{
		this->nodeBrufFunction_[currDest] = json::parse(infile);
		infile.close();
		string command = "rm " + filename;
		char removeFile[command.length() + 1];
		strcpy(removeFile, command.c_str());
		system(removeFile);
	}
	else
	{
		cout << "An Error happened reading the routing decisions file for " + to_string(currDest);
	}
}

double get_probability_if_this_route_is_chosen(Route *route)
{
	if (!useUncertainMode)
	{
		return 0;
	}

	ListElt *eltf = route->hops->first;

	UniboContact* first = (UniboContact*) eltf->data;

	int ts = getTsForStartOrCurrentTime(route->fromTime);
	vector<UniboContact*> hopsWithinTs;

	for (ListElt *elt = route->hops->first; elt != NULL; elt = elt->next)
	{
		UniboContact *currHop = (UniboContact*) elt->data;
		if (getTsForStartOrCurrentTime(currHop->fromTime) == ts)
		{
			hopsWithinTs.push_back(currHop);
		}
		else
		{
			break;
		}
	}

	int last_hop_destination = hopsWithinTs.back()->toNode;

	double successProbability = getNodeFutureDeliveryProbability(last_hop_destination, ts + 1);

	for (size_t i = 0; i < hopsWithinTs.size(); i++)
	{
		successProbability = successProbability * (1 - hopsWithinTs.at(i)->pf);
	}

	for (size_t i = 0; i < hopsWithinTs.size(); i++)
	{
		double currProbability = 1;

		for (size_t j = 0; j < i; j++)
		{
			currProbability = currProbability * (1 - hopsWithinTs.at(j)->pf);
		}

		currProbability = currProbability * hopsWithinTs.at(i)->pf *
				getNodeFutureDeliveryProbability(hopsWithinTs.at(i)->fromNode, ts + 1);

		successProbability = successProbability + currProbability;
	}

	return successProbability;
}

double get_probability_if_this_contact_is_chosen(UniboContact *contact, time_t earliestTransmissionTime)
{
	if (!useUncertainMode)
	{
		return 0;
	}

	int ts = getTsForStartOrCurrentTime(earliestTransmissionTime);

	double successProbability = (1 - contact->pf) * getNodeFutureDeliveryProbability(contact->toNode, ts + 1);

	successProbability = successProbability + (contact->pf * getNodeFutureDeliveryProbability(contact->fromNode, ts + 1));

	return successProbability;

}

double getNodeFutureDeliveryProbability(int carrierEid, int ts) //from CGRBRUFPowered
{
	string sTs = to_string(ts);
	string sCarrier = to_string(carrierEid);

	if (!useUncertainMode)
	{
		return 0;
	}

	if (currDest == carrierEid)
	{
		return 1.0;
	}

	if (ts == numOfTs)
	{
		if (currDest == carrierEid)
		{
			return 1.0;
		}
		else
		{
			return 0;
		}
	}
	try
	{
		double result = brufFunction.at(sTs).at(sCarrier);
		return result;
	} catch (...)
	{
		return 0;
	}
	//return brufFunction.at(sSource).at(sTarget).at(sTs).at(sCarrier);
}

int computeApplicableBacklog(unsigned long long neighbor, int priority, unsigned int ordinal, CgrScalar *CgrApplicableBacklog, CgrScalar *CgrTotalBacklog)
{
	int result = 0;
	int totalByte;
	int appByte;
	vector<int> totalSizes;
	vector<int> appSizes;

	//Pointers must not be allowed to be NULL
	if (CgrApplicableBacklog != NULL && CgrTotalBacklog != NULL)
	{
		totalSizes = sdrUnibo->getBundleSizesStoredToNeighbor(neighbor);
		appSizes = sdrUnibo->getBundleSizesStoredToNeighborWithHigherPriority(neighbor, priority == 2);
		totalByte = getTotalEVC(totalSizes);
		appByte = getTotalEVC(appSizes);
		loadCgrScalar(CgrTotalBacklog, totalByte);
		loadCgrScalar(CgrApplicableBacklog, appByte);
	}
	else
	{
		result = -1;
	}
	return result;
}

int getTotalEVC(vector<int> sizes)
{
	int result = 0;

	for (size_t i = 0; i < sizes.size(); i++)
	{
		result = result + computeBundleEVC(sizes.at(i));
	}
	return result;
}

int findMaxTs()
{

	return tsStartTimes[currDest].size() - 1;
}

void updateStartTimes(vector<Contact> *contacts)
{
	map<int, int> alreadySeen;
	tsStartTimes[currDest].clear();

	for (size_t i = 0; i < contacts->size(); i++)
	{
		int start = contacts->at(i).getStart();
		int end = contacts->at(i).getEnd();
		if (alreadySeen.find(start) == alreadySeen.end())
		{
			alreadySeen[start] = 1;
			tsStartTimes[currDest].push_back(start);
		}

		if (alreadySeen.find(end) == alreadySeen.end())
		{
			alreadySeen[end] = 1;
			tsStartTimes[currDest].push_back(end);
		}
	}

	sort(tsStartTimes[currDest].begin(), tsStartTimes[currDest].begin() + tsStartTimes[currDest].size());
	numOfTs = findMaxTs();

}

vector<int> getTsForContact(Contact *contact)
{
	int startTs = getTsForStartOrCurrentTime(contact->getStart());
	int endTs = getTsForEndTime(contact->getEnd());
	vector<int> tsValues;

	for (int i = startTs; i <= endTs; i++)
	{
		tsValues.push_back(i);
	}

	return tsValues;

}

