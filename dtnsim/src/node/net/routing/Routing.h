/*
 * Routing.h
 *
 *  Created on: Nov 8, 2016
 *      Author: juanfraire
 */

#ifndef SRC_NODE_NET_ROUTING_H_
#define SRC_NODE_NET_ROUTING_H_

#include <map>
#include <queue>
#include <limits>
#include <algorithm>
#include "ContactPlan.h"
#include "dtnsim_m.h"
#include "SdrModel.h"

using namespace omnetpp;
using namespace std;

class Routing
{
public:
	Routing()
	{
	}
	virtual ~Routing()
	{
	}

	// This is a pure virtual method (all routing must ate least
	// implement this function)
	virtual void routeBundle(BundlePkt *bundle, double simTime) = 0;
};

#endif /* SRC_NODE_NET_ROUTING_H_ */