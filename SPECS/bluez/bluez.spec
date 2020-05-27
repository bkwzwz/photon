Summary:	Bluetooth utilities
Name:		bluez
Version:	5.52
Release: 	1%{?dist}
License:	GPLv2+
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.kernel.org/pub/linux/bluetooth/bluez-%{version}.tar.xz
%define sha1 bluez=75e907922a62588c12d5642293403be0625b4d02

BuildRequires:  libical-devel
BuildRequires:  glib-devel
BuildRequires:  dbus-devel
BuildRequires:  systemd-devel

Requires:       dbus
Requires:       glib
Requires:       libical
Requires:       systemd

%description
Utilities for use in Bluetooth applications.
The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%package	devel
Summary:	Development libraries for Bluetooth applications
Group:		Development/System
Requires: %{name} = %{version}-%{release}

%description	devel
bluez-devel contains development libraries and headers for
use in Bluetooth applications.

%prep
%setup -q

%build
%configure \
	--enable-tools \
	--enable-library \
	--enable-usb \
	--enable-threads \
	--enable-monitor \
	--enable-obex \
	--enable-systemd \
	--enable-experimental \
	--enable-deprecated \
	--disable-cups

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/udev/hid2hci
%{_libexecdir}/bluetooth/obexd
%{_libexecdir}/bluetooth/bluetoothd
%{_datadir}/zsh/site-functions/_bluetoothctl
%{_libdir}/*.so.*
%{_libdir}/libbluetooth.la
%{_datadir}/dbus-1/system-services/org.bluez.service
%{_datadir}/dbus-1/services/org.bluez.obex.service
%{_libdir}/systemd/user/obex.service
%{_libdir}/systemd/system/bluetooth.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/bluetooth.conf
%{_libdir}/udev/rules.d/97-hid2hci.rules
%doc COPYING TODO

%files devel
%{_includedir}/bluetooth/*.h

%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/man/*

%changelog
* Mon Jan 6 2020 Ajay Kaher <akaher@vmware.com> 5.52-1
- Initial version


