NAME=coretests

pep8:
	@echo
	@echo "-----------"
	@echo "PEP8 issues"
	@echo "-----------"
	@pep8 --repeat --ignore=E203,E121,E122,E123,E124,E125,E126,E127,E128 . || true

clean:
	find -name "*.qm" -exec rm -r {} \;
	find -name "__pycache__" -type d -exec rm -r {} \; -prune
	rm -f $(NAME).zip

package: clean
	zip -9 -r $(NAME).zip $(NAME)
