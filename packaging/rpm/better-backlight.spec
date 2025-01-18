Name:           better-backlight
Version:        0.1.0
Release:        1%{?dist}
Summary:        A service that improves keyboard backlight management

License:        MIT

BuildArch:      x86_64
Requires:       python3-devel gcc python3-virtualenv

%global debug_package %{nil}

%description
A service that improves keyboard backlight management

%prep
# No source code to prepare

%build
# Nothing to build

%install
# Create the required directories
mkdir -p %{buildroot}/opt/better-backlight
mkdir -p %{buildroot}/opt/better-backlight/bin

# Install the service files
install -Dm 644 %{_sourcedir}/better-backlight.service \
    %{buildroot}/usr/lib/systemd/system/better-backlight.service
install -Dm 644 %{_sourcedir}/Pipfile \
    %{buildroot}/opt/better-backlight/Pipfile
install -Dm 644 %{_sourcedir}/Pipfile.lock \
    %{buildroot}/opt/better-backlight/Pipfile.lock
install -Dm 644 %{_sourcedir}/better-backlight.conf \
    %{buildroot}/etc/better-backlight.conf

cp -R %{_sourcedir}/better_backlight/ %{buildroot}/opt/better-backlight/
sed -i '1s|^|#!/opt/better-backlight/venv/bin/python\n|' %{buildroot}/opt/better-backlight/better_backlight/entrypoints/daemon.py

%files
/usr/lib/systemd/system/better-backlight.service
/etc/better-backlight.conf
/opt/better-backlight/
/opt/better-backlight/bin/
/opt/better-backlight/Pipfile
/opt/better-backlight/Pipfile.lock
/opt/better-backlight/better_backlight/

%post
export PIPENV_VERBOSITY=-1
cd /opt/better-backlight/

# Fresh install, let's create virtualenv
if [ $1 -eq 1 ]; then
    python3 -m venv /opt/better-backlight/venv
fi

ln -s /opt/better-backlight/better_backlight/entrypoints/daemon.py /opt/better-backlight/bin/better-backlight
chmod +x /opt/better-backlight/bin/better-backlight

# Dependencies installation. Idempotent.
source /opt/better-backlight/venv/bin/activate
pip install pipenv
pipenv install

if [ $1 -eq 1 ]; then
    systemctl enable better-backlight
    systemctl start better-backlight
else
    systemctl restart better-backlight
fi

%postun
if [ $1 -eq 0 ]; then
    rm -rf /opt/better-backlight/
    systemctl stop better-backlight
    systemctl disable better-backlight
    systemctl daemon-reload
fi

%changelog
* Sat Jan 18 2025 Yevhen Prodan <mora9715@gmail.com> - 0.1.0-1
- Add logging
- Add configuration
- Add more input devices support
* Wed Jan 15 2025 Yevhen Prodan <mora9715@gmail.com> - 0.0.1-1
- Initial RPM release
