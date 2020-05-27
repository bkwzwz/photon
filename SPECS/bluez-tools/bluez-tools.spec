Summary:       A set of tools to manage bluetooth devices for linux
Name:          bluez-tools
Version:       0.2.0.20140808
Release:       1%{?dist}
License:       GPL
Group:         Applications/Communication
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://code.google.com/p/bluez-tools/
Source0:       https://github.com/khvzak/bluez-tools.git/master/bluez-tools-%{version}.tar.gz
%define sha1 bluez-tools=a24245523f4d87d8a11e2dd41babc1aade1e0870


BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel

Requires:      bluez

%description
A set of tools to manage bluetooth devices for linux.

%prep
%setup -q

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_bindir}/bt-adapter
%{_bindir}/bt-agent
%{_bindir}/bt-device
%{_bindir}/bt-network
%{_bindir}/bt-obex
%{_mandir}/man1/bt-adapter.1*
%{_mandir}/man1/bt-agent.1*
%{_mandir}/man1/bt-device.1*
%{_mandir}/man1/bt-network.1*
%{_mandir}/man1/bt-obex.1*
%doc AUTHORS COPYING

%changelog
* Mon Jan 6 2020 Ajay Kaher <akaher@vmware.com> 0.2.0.20140808-1
- Initial version
