# THIS PROJECT IS DEPRECATED

I apologize for any inconvenience. All development effort has moved to the
[layer-docker](https://github.com/juju-solutions/layer-docker) repository. 

While we have strived to maintain charm compatibility with the layer-docker
approach, there are some nuances that just wont be right. However for the 
intrepid, if you are certain you know what you are doing:

- clone the layer-docker source
- Build a replacement docker charm
- upgrade and switch from the docker-charm to your freshly built layer-docker based charm

    git clone https://github.com/juju-solutions/layer-docker
    cd layer-docker
    charm build
    juju upgrade-charm docker --switch local:trusty/docker


## YOUR MILEAGE MAY VARY WITH THIS APPROACH! You have been warned!
