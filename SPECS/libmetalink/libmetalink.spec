Summary:       A Metalink library written in C language
Name:          libmetalink
Version:       0.1.3
Release:       1%{?dist}
Group:         Development/Libraries
Vendor:        VMware, Inc.
License:       MIT
URL:           https://launchpad.net/%{name}
Source0:       %{url}/trunk/%{name}-%{version}/+download/%{name}-%{version}.tar.bz2
%define sha1 %{name}-%{version}=20ccbea4b495d60ab6d9dd3e40b3a429cfa2584b
Distribution:  Photon
Requires:      expat
BuildRequires: expat-devel

%description
A Metalink library written in C language.

%package devel
Summary:    Development files for libmetalink 
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for libmetalink

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
install -Dm644 COPYING %{buildroot}%{_defaultlicensedir}/%{name}-%{version}/LICENSE

%post

    /sbin/ldconfig

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

%clean
rm -rf %{buildroot}/*

%files
%{_defaultlicensedir}/*
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/*

%changelog
*  Fri Jan 24 2020 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1.3-1
-  Initial
