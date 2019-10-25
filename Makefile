build:
	@python3 Tora/CompileSrc.py project.conf
	@python3 Tora/GenerateFinal.py project.conf
	@python3 Tora/PackageCode.py project.conf

clean:
	@python3 Tora/Clean.py project.conf

zip:
	@make clean
	@zip zipfile project.zip ./*
