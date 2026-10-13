DESCRIPTION = "Serial OS Configuration"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=990cdac95cb92035c2df58cadf9a387e"

S = "${UNPACKDIR}"

SRC_URI = "\
    file://config.yaml \
    file://LICENSE \
"

do_install() {
    install -d -m 755 ${D}/serialos
    install -m 0644 ${S}/config.yaml ${D}/serialos/
}

FILES:${PN} = "/serialos"