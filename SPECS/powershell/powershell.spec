Summary:        PowerShell is an automation and configuration management platform.
Name:           powershell
Version:        7.0.0
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://microsoft.com/powershell
Group:          shells
Source0:        %{name}-%{version}.tar.gz
%define sha1    powershell=b56eac631c7d3085d93ccc5e2c517422be0e26d4
Source1:        %{name}-native-%{version}.tar.gz
%define sha1    powershell-native=7606e94dc5691d6d9297b5c4452a08728c93d526
Source2:        %{name}-linux-%{version}-x64.tar.gz
%define sha1    powershell-linux=d4d4f9e998e41cb57c52421fe20103d32dbf8af0
Source3:        build.sh
Source4:        Microsoft.PowerShell.SDK.csproj.TypeCatalog.targets

BuildArch:      x86_64
BuildRequires:  dotnet-sdk = 3.1.201
BuildRequires:  dotnet-runtime = 3.1.3
BuildRequires:  psmisc
BuildRequires:  cmake
BuildRequires:  clang
BuildRequires:  git
Requires:       icu

#gallery download scripts will fail without this
Requires:       zlib-devel

%description
PowerShell is an automation and configuration management platform.
It consists of a cross-platform command-line shell and associated scripting language.

%prep
%setup -qn PowerShell-%{version}
%setup -qcTDa 1 -n PowerShell-Native
%setup -qcTDa 2 -n %{name}-linux-%{version}-x64

%build
cd %{_builddir}/PowerShell-%{version}
sed -i -e '/refs\/tags\/v%{version}/{n;q}' .git/packed-refs
cp %{SOURCE3} .
cp %{SOURCE4} src
chmod +x ./build.sh
./build.sh
cd %{_builddir}/PowerShell-Native/powershell-native-%{version}
pushd src/libpsl-native
cmake -DCMAKE_BUILD_TYPE=Debug .
make -j

%install
cd %{_builddir}/PowerShell-%{version}
rm -rf src/powershell-unix/bin/{Debug, Linux}
mkdir -p %{buildroot}%{_libdir}/powershell
mkdir -p %{buildroot}%{_docdir}/powershell
mv bin/ThirdPartyNotices.txt %{buildroot}%{_docdir}/powershell
mv bin/LICENSE.txt %{buildroot}%{_docdir}/powershell
cp -r bin/* %{buildroot}/%{_libdir}/powershell
rm -f %{buildroot}/%{_libdir}/powershell/libpsl-native.so
cp -rf %{_builddir}/PowerShell-Native/powershell-native-%{version}/src/powershell-unix/libpsl-native.so %{buildroot}/%{_libdir}/powershell
mkdir -p %{buildroot}%{_bindir}
chmod 0755 %{buildroot}/%{_libdir}/powershell/pwsh
ln -sf %{_libdir}/powershell/pwsh %{buildroot}%{_bindir}/pwsh
mkdir -p %{buildroot}%{_libdir}/powershell/ref
cp %{_builddir}/powershell-linux-%{version}-x64/ref/* %{buildroot}%{_libdir}/powershell/ref
cp -r %{_builddir}/powershell-linux-%{version}-x64/Modules/{PSReadLine,PowerShellGet,PackageManagement} \
%{buildroot}%{_libdir}/powershell/Modules

%check
cd %{_builddir}/PowerShell-%{version}/test/xUnit
dotnet test
export LANG=en_US.UTF-8
cd %{_builddir}/PowerShell-Native/powershell-native-%{version}/src/libpsl-native
make test

%post
#in case of upgrade, delete the soft links
if [ $1 -eq 2 ] ; then
    pushd %{_libdir}/powershell/ref
    find -type l -exec unlink {} \;
    popd
fi
grep -qF /usr/bin/pwsh /etc/shells || echo "/usr/bin/pwsh" >> /etc/shells

%preun
#remove on uninstall
if [ $1 -eq 0 ]; then
  sed -i '\/usr\/bin\/pwsh/d' /etc/shells
fi

%files
    %defattr(-,root,root,0755)
    %exclude %{_libdir}/debug
    %{_libdir}/*
    %{_bindir}/pwsh
    %{_docdir}/*

%changelog
*   Sat Apr 11 2020 Shreyas B <shreyasb@vmware.com> 7.0.0-1
-   Upgrade powershell to 7.0.0
*   Thu Dec 19 2019 Shreyas B <shreyasb@vmware.com> 6.2.3-5
-   Adding make check for powershell & powershell-native.
-   Fix Test failre in libpsl-native/test/test-locale.cpp.
*   Mon Dec 16 2019 Shreyas B <shreyasb@vmware.com> 6.2.3-4
-   Build PowerShell with locally build "libpsl-native.so" from PowerShell-Native(6.2.0).
*   Wed Dec 04 2019 Tapas Kundu <tkundu@vmware.com> 6.2.3-3
-   Fixed ref folder to have right dlls
*   Tue Dec 03 2019 Tapas Kundu <tkundu@vmware.com> 6.2.3-2
-   Fix post in case of upgrade
*   Wed Nov 13 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.2.3-1
-   update to 6.2.3
-   refactor build script
-   include PSReadLine, PowerShellGet and PackageManagement modules
*   Wed Feb 13 2019 Ajay Kaher <akaher@vmware.com> 6.1.1-2
-   Fix version mismatch issue.
*   Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 6.1.1-1
-   upgrade version to 6.1.1
*   Thu Sep 27 2018 Ajay Kaher <akaher@vmware.com> 6.0.1-2
-   upgrade version of dotnet-runtime
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0.1-1
-   Initial build for photon
