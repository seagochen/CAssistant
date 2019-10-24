build:
	@python3 Tora/compilesrc.py project.conf
	@python3 Tora/compileout.py project.conf

generate:
	@python3 Tora/compileout.py project.conf

clean:
	@python3 Tora/cleanpro.py project.conf

zip:
	@zip zipfile project.zip ./*
