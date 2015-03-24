SUBDIRS = webExtractor

bin_SCRIPTS = blogPrint
CLEANFILES = $(bin_SCRIPT)
EXTRA_DIST = blogPrint.in

do_subs = sed -e 's,[@]pythondir[@],$(pythondir),g' \
              -e 's,[@]PACKAGE[@],$(PACKAGE),g' \
              -e 's,[@]VERSION[@],$(VERSION),g'

blogPrint: blogPrint.in Makefile
	$(do_subs) < $(srcdir)/blogPrint.in > blogPrint
	chmod +x blogPrint
