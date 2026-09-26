SUMMARY = "SerialOS application"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=990cdac95cb92035c2df58cadf9a387e"

PV = "0.1.0"

inherit externalsrc
inherit cargo
inherit cargo-update-recipe-crates

# externalsrc requires a literal absolute path, so expand TOPDIR at parse time
EXTERNALSRC:pn-${PN} := "${TOPDIR}/../../software"

require ${BPN}-crates.inc

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${B}/target/${CARGO_TARGET_SUBDIR}/software ${D}${bindir}/software
}

FILES:${PN} = "${bindir}/software"
