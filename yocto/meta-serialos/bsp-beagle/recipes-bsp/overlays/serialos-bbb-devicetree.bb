inherit devicetree

COMPATIBLE_MACHINE = "beagle-serialos"

SRC_URI = " \
    file://serialos-bbb.dts \
"

# ti omap dtsi files live two levels deep under dts/ti/omap
DT_INCLUDE:append = " ${STAGING_KERNEL_DIR}/arch/${ARCH}/boot/dts/ti/omap"