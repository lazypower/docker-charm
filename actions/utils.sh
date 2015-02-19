function rmi-all-free(){
    docker rmi $(docker images -q --filter "dangling=true")
}

function rm-stopped-containers(){
    docker rm $(docker ps -a -q)
}
