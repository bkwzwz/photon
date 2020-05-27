%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:	The gcovr command provides a utility for managing the use of the GNU gcov utility
Name:		gcovr
Version:	4.1
Release:	3%{?dist}
License:	BSD Clause-3
URL:		http://gcovr.com/
Source0:	https://github.com/gcovr/gcovr/archive/%{name}-%{version}.tar.gz
%define sha1 gcovr=69520213d49bc46966fa23de336cc11b64a0fc2e
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:	python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python-pip
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python-pytest
BuildRequires:  python3-pytest
BuildRequires:  python-six
BuildRequires:  python3-six
BuildRequires:  python-attrs
BuildRequires:  python3-attrs
BuildRequires:  python-xml
%endif
Requires:       python2
Requires:       python2-libs
Buildarch:	noarch
%description
The gcovr command provides a utility for managing the use of the GNU gcov utility and generating summarized code coverage results. This command is inspired by the Python coverage.py package, which provides a similar utility in Python. Gcovr produces either compact human-readable summary reports, machine readable XML reports or a simple HTML summary.

%package -n     python3-gcovr
Summary:        python3-gcovr
Requires:       python3
Requires:       python3-libs
%description -n python3-gcovr

%prep
%setup -q
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build

pushd ../p3dir
python3 setup.py build
popd
%install
pushd ../p3dir
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
popd
mv %{buildroot}/%{_bindir}/gcovr  %{buildroot}/%{_bindir}/gcovr3

python2 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}


%check
pip install funcsigs pathlib2 pluggy utils atomicwrites more_itertools pyutilib
python2 setup.py test
pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 funcsigs pathlib2 pluggy utils atomicwrites more_itertools
$easy_install_3 pyutilib
python3 setup.py test
popd

%files
%defattr(-,root,root)
%doc README.rst LICENSE.txt CHANGELOG.rst
%{python2_sitelib}*
%{_bindir}/gcovr

%files -n python3-gcovr
%defattr(-,root,root)
%doc README.rst LICENSE.txt CHANGELOG.rst
%{_bindir}/gcovr3
%{python3_sitelib}*

%changelog
*   Wed Sep 18 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 4.1-3
-   Fix for make check failure using pip instead of easy_install for python2
*   Wed Nov 21 2018 Ashwin H <ashwinh@vmware.com> 4.1-2
-   Fix gcovr %check
*   Tue Sep 18 2018 Sujay G <gsujay@vmware.com> 4.1-1
-   Bump gcovr version to 4.1
*   Fri Jun 09 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.3-1
-   Initial build. First version
