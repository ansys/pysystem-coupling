# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXERRWARN = -W --keep-going
SPHINXOPTS    = -v -j auto $(SPHINXERRWARN) -w build_errors.txt -N
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@python datamodel_rstgen.py
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# customized clean due to examples gallery
clean:
	rm -rf $(BUILDDIR)/*
	rm -rf $(SOURCEDIR)/examples
	find . -type d -name "_autosummary" -exec rm -rf {} +

# Create PDF
pdf:
	@$(SPHINXBUILD) -M latex "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cd $(BUILDDIR)/latex && latexmk -r latexmkrc -pdf *.tex -interaction=nonstopmode -f || true
	(test -f $(BUILDDIR)/latex/ansys-systemcoupling-core*.pdf && echo pdf exists) || exit 1
