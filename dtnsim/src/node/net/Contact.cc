#include <Contact.h>

Contact::Contact(int id, double start, double end, int sourceEid, int destinationEid, double dataRate)
{
	this->id_ = id;
	this->start_ = start;
	this->end_ = end;
	this->sourceEid_ = sourceEid;
	this->destinationEid_ = destinationEid;
	this->dataRate_ = dataRate;
}

Contact::~Contact()
{

}

double Contact::getDataRate() const
{
	return dataRate_;
}

int Contact::getDestinationEid() const
{
	return destinationEid_;
}

int Contact::getId() const
{
	return id_;
}

double Contact::getResidualCapacity() const
{
	return residualCapacity_;
}

int Contact::getSourceEid() const
{
	return sourceEid_;
}

double Contact::getStart() const
{
	return start_;
}

double Contact::getEnd() const
{
	return end_;
}

double Contact::getDuration() const
{
	return (end_ - start_);
}
