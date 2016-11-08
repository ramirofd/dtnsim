//
// Generated file, do not edit! Created by nedtool 5.0 from dtnsim.msg.
//

#ifndef __DTNSIM_M_H
#define __DTNSIM_M_H

#include <omnetpp.h>

// nedtool version check
#define MSGC_VERSION 0x0500
#if (MSGC_VERSION!=OMNETPP_VERSION)
#    error Version mismatch! Probably this file was generated by an earlier version of nedtool: 'make clean' should help.
#endif



// cplusplus {{
    typedef std::list<int> List;
// }}

/**
 * Class generated from <tt>dtnsim.msg:8</tt> by nedtool.
 * <pre>
 * packet Bundle
 * {
 *     int sourceEid;
 *     int destinationEid;
 * 
 *     simtime_t creationTimestamp;
 *     simtime_t ttl;
 * 
 *     List originalRoute;
 *     List takenRoute;
 * }
 * </pre>
 */
class Bundle : public ::omnetpp::cPacket
{
  protected:
    int sourceEid;
    int destinationEid;
    ::omnetpp::simtime_t creationTimestamp;
    ::omnetpp::simtime_t ttl;
    List originalRoute;
    List takenRoute;

  private:
    void copy(const Bundle& other);

  protected:
    // protected and unimplemented operator==(), to prevent accidental usage
    bool operator==(const Bundle&);

  public:
    Bundle(const char *name=nullptr, int kind=0);
    Bundle(const Bundle& other);
    virtual ~Bundle();
    Bundle& operator=(const Bundle& other);
    virtual Bundle *dup() const {return new Bundle(*this);}
    virtual void parsimPack(omnetpp::cCommBuffer *b) const;
    virtual void parsimUnpack(omnetpp::cCommBuffer *b);

    // field getter/setter methods
    virtual int getSourceEid() const;
    virtual void setSourceEid(int sourceEid);
    virtual int getDestinationEid() const;
    virtual void setDestinationEid(int destinationEid);
    virtual ::omnetpp::simtime_t getCreationTimestamp() const;
    virtual void setCreationTimestamp(::omnetpp::simtime_t creationTimestamp);
    virtual ::omnetpp::simtime_t getTtl() const;
    virtual void setTtl(::omnetpp::simtime_t ttl);
    virtual List& getOriginalRoute();
    virtual const List& getOriginalRoute() const {return const_cast<Bundle*>(this)->getOriginalRoute();}
    virtual void setOriginalRoute(const List& originalRoute);
    virtual List& getTakenRoute();
    virtual const List& getTakenRoute() const {return const_cast<Bundle*>(this)->getTakenRoute();}
    virtual void setTakenRoute(const List& takenRoute);
};

inline void doParsimPacking(omnetpp::cCommBuffer *b, const Bundle& obj) {obj.parsimPack(b);}
inline void doParsimUnpacking(omnetpp::cCommBuffer *b, Bundle& obj) {obj.parsimUnpack(b);}

/**
 * Class generated from <tt>dtnsim.msg:19</tt> by nedtool.
 * <pre>
 * message TrafficGeneratorMsg
 * {
 *     int bundlesNumber;
 *     int destinationEid;
 *     int size;
 *     int ttl;
 *     int interval;
 * }
 * </pre>
 */
class TrafficGeneratorMsg : public ::omnetpp::cMessage
{
  protected:
    int bundlesNumber;
    int destinationEid;
    int size;
    int ttl;
    int interval;

  private:
    void copy(const TrafficGeneratorMsg& other);

  protected:
    // protected and unimplemented operator==(), to prevent accidental usage
    bool operator==(const TrafficGeneratorMsg&);

  public:
    TrafficGeneratorMsg(const char *name=nullptr, int kind=0);
    TrafficGeneratorMsg(const TrafficGeneratorMsg& other);
    virtual ~TrafficGeneratorMsg();
    TrafficGeneratorMsg& operator=(const TrafficGeneratorMsg& other);
    virtual TrafficGeneratorMsg *dup() const {return new TrafficGeneratorMsg(*this);}
    virtual void parsimPack(omnetpp::cCommBuffer *b) const;
    virtual void parsimUnpack(omnetpp::cCommBuffer *b);

    // field getter/setter methods
    virtual int getBundlesNumber() const;
    virtual void setBundlesNumber(int bundlesNumber);
    virtual int getDestinationEid() const;
    virtual void setDestinationEid(int destinationEid);
    virtual int getSize() const;
    virtual void setSize(int size);
    virtual int getTtl() const;
    virtual void setTtl(int ttl);
    virtual int getInterval() const;
    virtual void setInterval(int interval);
};

inline void doParsimPacking(omnetpp::cCommBuffer *b, const TrafficGeneratorMsg& obj) {obj.parsimPack(b);}
inline void doParsimUnpacking(omnetpp::cCommBuffer *b, TrafficGeneratorMsg& obj) {obj.parsimUnpack(b);}

/**
 * Class generated from <tt>dtnsim.msg:27</tt> by nedtool.
 * <pre>
 * message ContactMsg
 * {
 *     int id;
 *     double dataRate;
 *     simtime_t start;
 *     simtime_t end;
 *     simtime_t duration;
 *     int sourceEid;
 *     int destinationEid;
 * }
 * </pre>
 */
class ContactMsg : public ::omnetpp::cMessage
{
  protected:
    int id;
    double dataRate;
    ::omnetpp::simtime_t start;
    ::omnetpp::simtime_t end;
    ::omnetpp::simtime_t duration;
    int sourceEid;
    int destinationEid;

  private:
    void copy(const ContactMsg& other);

  protected:
    // protected and unimplemented operator==(), to prevent accidental usage
    bool operator==(const ContactMsg&);

  public:
    ContactMsg(const char *name=nullptr, int kind=0);
    ContactMsg(const ContactMsg& other);
    virtual ~ContactMsg();
    ContactMsg& operator=(const ContactMsg& other);
    virtual ContactMsg *dup() const {return new ContactMsg(*this);}
    virtual void parsimPack(omnetpp::cCommBuffer *b) const;
    virtual void parsimUnpack(omnetpp::cCommBuffer *b);

    // field getter/setter methods
    virtual int getId() const;
    virtual void setId(int id);
    virtual double getDataRate() const;
    virtual void setDataRate(double dataRate);
    virtual ::omnetpp::simtime_t getStart() const;
    virtual void setStart(::omnetpp::simtime_t start);
    virtual ::omnetpp::simtime_t getEnd() const;
    virtual void setEnd(::omnetpp::simtime_t end);
    virtual ::omnetpp::simtime_t getDuration() const;
    virtual void setDuration(::omnetpp::simtime_t duration);
    virtual int getSourceEid() const;
    virtual void setSourceEid(int sourceEid);
    virtual int getDestinationEid() const;
    virtual void setDestinationEid(int destinationEid);
};

inline void doParsimPacking(omnetpp::cCommBuffer *b, const ContactMsg& obj) {obj.parsimPack(b);}
inline void doParsimUnpacking(omnetpp::cCommBuffer *b, ContactMsg& obj) {obj.parsimUnpack(b);}

/**
 * Class generated from <tt>dtnsim.msg:37</tt> by nedtool.
 * <pre>
 * message FreeChannelMsg
 * {
 *     int neighborEid;
 *     int contactId;
 * }
 * </pre>
 */
class FreeChannelMsg : public ::omnetpp::cMessage
{
  protected:
    int neighborEid;
    int contactId;

  private:
    void copy(const FreeChannelMsg& other);

  protected:
    // protected and unimplemented operator==(), to prevent accidental usage
    bool operator==(const FreeChannelMsg&);

  public:
    FreeChannelMsg(const char *name=nullptr, int kind=0);
    FreeChannelMsg(const FreeChannelMsg& other);
    virtual ~FreeChannelMsg();
    FreeChannelMsg& operator=(const FreeChannelMsg& other);
    virtual FreeChannelMsg *dup() const {return new FreeChannelMsg(*this);}
    virtual void parsimPack(omnetpp::cCommBuffer *b) const;
    virtual void parsimUnpack(omnetpp::cCommBuffer *b);

    // field getter/setter methods
    virtual int getNeighborEid() const;
    virtual void setNeighborEid(int neighborEid);
    virtual int getContactId() const;
    virtual void setContactId(int contactId);
};

inline void doParsimPacking(omnetpp::cCommBuffer *b, const FreeChannelMsg& obj) {obj.parsimPack(b);}
inline void doParsimUnpacking(omnetpp::cCommBuffer *b, FreeChannelMsg& obj) {obj.parsimUnpack(b);}


#endif // ifndef __DTNSIM_M_H
