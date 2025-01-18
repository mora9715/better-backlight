format:
	black ./better_backlight
	isort ./better_backlight

lint:
	pylint ./better_backlight


build-rpm:
	rm -rf ~/rpmbuild/SOURCES/*
	cp Pipfile* ~/rpmbuild/SOURCES/
	cp packaging/usr/lib/systemd/system/better-backlight.service ~/rpmbuild/SOURCES/
	cp packaging/etc/better-backlight.conf ~/rpmbuild/SOURCES/
	cp -R better_backlight ~/rpmbuild/SOURCES/

	cp packaging/rpm/better-backlight.spec ~/rpmbuild/SPECS/

	rpmbuild -ba ~/rpmbuild/SPECS/better-backlight.spec