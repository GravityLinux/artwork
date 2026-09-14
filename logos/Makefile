SOURCES=$(wildcard src/*.svg)
# ICNS containers require square artwork; horizontal lockups are distributed as
# SVG/PNG only.
ICNS_SOURCES=$(filter-out %_horizontal.svg %_horizontal_darkbg.svg %_horizontal_mono.svg,$(SOURCES))
TARGETS=$(patsubst src/%.svg,svg/%.svg,$(SOURCES)) \
	$(patsubst src/%.svg,png_1x/%.png,$(SOURCES)) \
	$(patsubst src/%.svg,png_2x/%.png,$(SOURCES)) \
	$(patsubst src/%.svg,png_512/%.png,$(SOURCES)) \
	$(patsubst src/%.svg,png_256/%.png,$(SOURCES)) \
	$(patsubst src/%.svg,png_128/%.png,$(SOURCES)) \
	$(patsubst src/%.svg,png_64/%.png,$(SOURCES)) \
	$(patsubst src/%.svg,png_48/%.png,$(SOURCES)) \
	$(patsubst src/%.svg,png_32/%.png,$(SOURCES)) \
	$(patsubst src/%.svg,png_16/%.png,$(SOURCES)) \
	$(patsubst src/%.svg,png_16/%.png,$(SOURCES)) \
	$(patsubst src/%.svg,icns/%.icns,$(ICNS_SOURCES)) \
	boot_logo.ppm

all: $(TARGETS)

svg/%.svg : src/%.svg
	inkscape $< --vacuum-defs --export-plain-svg --export-filename=$@

png_1x/%.png : src/%.svg
	inkscape $< --export-dpi 96 --export-filename=$@

png_2x/%.png : src/%.svg
	inkscape $< --export-dpi 192 --export-filename=$@

png_512/%.png : src/%.svg
	inkscape $< --export-width 512 --export-filename=$@

png_256/%.png : src/%.svg
	inkscape $< --export-width 256 --export-filename=$@

png_128/%.png : src/%.svg
	inkscape $< --export-width 128 --export-filename=$@

png_64/%.png : src/%.svg
	inkscape $< --export-width 64 --export-filename=$@

png_48/%.png : src/%.svg
	inkscape $< --export-width 48 --export-filename=$@

png_32/%.png : src/%.svg
	inkscape $< --export-width 32 --export-filename=$@

png_16/%.png : src/%.svg
	inkscape $< --export-width 16 --export-filename=$@

icns/%.icns: png_16/%.png png_32/%.png png_48/%.png png_128/%.png png_256/%.png png_512/%.png
	png2icns $@ png_16/$*.png png_32/$*.png png_48/$*.png png_128/$*.png png_256/$*.png png_512/$*.png

boot_logo.ppm: src/GravityLinux_logomark.svg
	@task_tmp=$$(mktemp --suffix=.png); trap 'rm -f "$$task_tmp"' EXIT; \
	inkscape src/GravityLinux_logomark.svg --export-area=24:24:550:550 \
		--export-width 80 --export-background=black --export-type=png \
		--export-filename="$$task_tmp"; \
	pngtopnm "$$task_tmp" | ppmquant 224 | pnmtoplainpnm > $@
