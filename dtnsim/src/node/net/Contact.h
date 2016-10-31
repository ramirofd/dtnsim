#ifndef CONTACT_H_
#define CONTACT_H_

class Contact
{
public:

	Contact(int id, double start, double end, int sourceEid, int destinationEid, double dataRate);
	virtual ~Contact();
	double getDataRate() const;
	int getDestinationEid() const;
	int getId() const;
	double getResidualCapacity() const;
	int getSourceEid() const;
	double getStart() const;
	double getEnd() const;
	double getDuration() const;

private:

	int id_;
	double start_;
	double end_;
	int sourceEid_;
	int destinationEid_;
	double dataRate_;
	double residualCapacity_;
};

#endif /* CONTACT_H_ */
