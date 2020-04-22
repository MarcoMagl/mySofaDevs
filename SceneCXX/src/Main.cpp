#include <sstream>
using std::ostringstream ;
#include <fstream>

#include <sofa/helper/ArgumentParser.h>
#include <SofaSimulationCommon/common.h>
#include <sofa/simulation/Node.h>
#include <sofa/helper/system/PluginManager.h>
#include <sofa/simulation/config.h> // #defines SOFA_HAVE_DAG (or not)
#include <SofaSimulationCommon/init.h>
#include <SofaSimulationTree/init.h>
#include <SofaSimulationTree/TreeSimulation.h>

#include <SofaComponentCommon/initComponentCommon.h>
#include <SofaComponentBase/initComponentBase.h>
#include <SofaComponentGeneral/initComponentGeneral.h>
#include <SofaComponentAdvanced/initComponentAdvanced.h>
#include <SofaComponentMisc/initComponentMisc.h>
#include <sofa/helper/BackTrace.h>

// Add any other includes needed by your scene
// #include<path_to/myComponent.h>
// ...

int main(int argc, char** argv)
{
    sofa::helper::BackTrace::autodump();
    ExecParams::defaultInstance()->setAspectID(0);

    // here you can init the GUI you wish
    // as an example, see : applications/projects/runSofa/Main.cpp

    sofa::simulation::tree::init();
    sofa::component::initComponentBase();
    sofa::component::initComponentCommon();
    sofa::component::initComponentGeneral();
    sofa::component::initComponentAdvanced();
    sofa::component::initComponentMisc();

    sofa::simulation::setSimulation(new sofa::simulation::tree::TreeSimulation());

    std::ostringstream no_error_message;
    sofa::helper::system::PluginManager::getInstance().loadPlugin("MyPlugin",&no_error_message);
    sofa::helper::system::PluginManager::getInstance().init();

    // Here start the description of your scene in C++

    // you can create nodes
    sofa::simulation::tree::GNode* groot = new sofa::simulation::tree::GNode;
    groot->setName ("root");
    sofa::defaulttype::Vec3d g = sofa::defaulttype::Vec3d (0,-9.81,0);
    groot->setGravityInWorld(g);

    // you can create components in these nodes
    addMyComponent(groot);

    // you can add new child nodes and repeat the process to build your scene
    sofa::simulation::tree::GNode* childNode = new sofa::simulation::tree::GNode;
    childNode->setName( "child_of_root" );\r
    groot->addChild(childNode);

    addMyComponent(childNode);

    sofa::simulation::getSimulation()->init(groot.get());
    

    // Run the simulation
    groot->setAnimate(true);

    // close the simulation
    if (groot!=NULL)
        sofa::simulation::getSimulation()->unload(groot);

    sofa::simulation::common::cleanup();
    sofa::simulation::tree::cleanup();
    return 0;
}

// this function illustrates how to add a component to a node
myComponent *addMyComponent(sofa::simulation::tree::GNode *node) {

    myComponent* myComp = new myComponent;
    myComp->setName ("myComponentName");
    myComp->addTag ((Tag)"myTag");
    myComp->d_data.setValue(0.02); // any public data of the component can thus be defined
    node->addObject (myComp);
    
    return (myComponent *)solver;
}