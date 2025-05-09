# Megaserial OS

I guess this is an OS which brings things you need for making your own embedded linux application on some different hardware.

- Upgrading should be rock solid, atomic, and support nice things like roll back in the case of a failed upgrade.
- Logging support.
- Traces when things crash.
- Storage for system configuration, user configuration, and performant database storage.
- Make use of containerization for user applications.
- Support user application in the base system.

### Upgrading

There are a bunch of different upgrading solutions for linux: Mender, Rauc, and SWUpdate to name a few, which all have their ups and downs
