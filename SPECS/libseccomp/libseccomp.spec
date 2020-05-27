Summary:       Enhanced seccomp library
Name:          libseccomp
Version:       2.4.3
Release:       1%{?dist}
License:       LGPLv2
Group:         System Environment/Libraries
Source0:       https://github.com/seccomp/libseccomp/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha1 libseccomp=477a66a6c5a32e585adaf90961994641de313247
Url:           https://github.com/seccomp/libseccomp/wiki
Vendor:        VMware, Inc.
Distribution:  Photon

BuildRequires: which

%description
The libseccomp library provides an easy to use, platform independent, interface
to the Linux Kernel syscall filtering mechanism: seccomp. The libseccomp API
is designed to abstract away the underlying BPF based syscall filter language
and present a more conventional function-call based filtering interface that
should be familiar to, and easily adopted by application developers.

%package devel
Summary:  Development files used to build applications with libseccomp support
Group:    Development/Libraries
Provides: pkgconfig(libseccomp)

%description devel
The libseccomp-devel package contains the libraries and header files
needed for developing secure applications.

%prep
%autosetup

%build
%configure
make V=1 %{?_smp_mflags}

%install
rm -rf "%{buildroot}"
make V=1 DESTDIR="%{buildroot}" install

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE
%doc CREDITS
%doc README.md
%{_libdir}/libseccomp.so.*

%files devel
%{_includedir}/seccomp.h
%{_includedir}/seccomp-syscalls.h
%{_libdir}/libseccomp.so
%{_libdir}/libseccomp.a
%{_libdir}/libseccomp.la
%{_libdir}/pkgconfig/libseccomp.pc
%{_bindir}/scmp_sys_resolver
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
*  Thu May 7 2020 Susant Sahani <ssahani@vmware.com> 2.4.3-1
-  Updated to version 2.4.3.
*  Wed Jan 9 2019 Michelle Wang <michellew@vmware.com> 2.3.3-2
-  Fix make check for libseccomp.
*  Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 2.3.3-1
-  Updated to version 2.3.3.
*  Tue Apr 11 2017 Harish Udaiya KUmar <hudaiyakumar@vmware.com> 2.3.2-1
-  Updated to version 2.3.2.
*  Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.3-2
-  GA - Bump release of all rpms.
*  Sat Jan 16 2016 Fabio Rapposelli <fabio@vmware.com> - 2.2.3-1
-  First release of the package.
