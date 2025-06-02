 
# The LSPHP
LiteSpeed PHP is an optimized compilation of PHP built to work with LiteSpeed products through the LiteSpeed SAPI.

## Prebuilt packages 
The easiest way to get up and running with PHP is to use the LiteSpeed Repository. The LiteSpeed Repository comes with prebuilt PHP packages with LiteSpeed support built in.
[Document Link](https://docs.litespeedtech.com/lsws/extapp/php/getting_started/)

## Building custom PHP from local
To build a custom package on a local server. 
1. Install git, docker, pbuilder and debhelper
2. Start container with command, `docker run -d --name packagebuild --user root --cap-add SYS_ADMIN --security-opt seccomp=unconfined --security-opt apparmor=unconfined -it eggcold/centos-build`
3. Login to the container: `docker exec -it packagebuild bash`
4. clone the repo or your forked repo, `git clone https://github.com/litespeedrepo/centos-lsphp.git`
5. Switch branch, e.g. php84: `git checkout php84`
6. Run example command to build, e.g. apcu package for epel-9 distribution: `./build.sh apcu 9 x86_64`
7. Result rpm will be stored under, e.g. **packaging/build/apcu/5.1.24/result/epel-9-x86_64/** folder

## Support, Feedback, and Collaboration

* Join [the GoLiteSpeed Slack community](https://litespeedtech.com/slack) for real-time discussion
* Post to [the LiteSpeed Forums](https://litespeedtech.com/support/forum/) for community support
* Report problems with these docs in [the project's Issues](https://github.com/litespeedrepo/debian-lsphp/issues)
* Contribute to these docs with [a Pull Request](https://github.com/litespeedrepo/debian-lsphp/pulls). This project is intended to be a safe, welcoming space for collaboration.
