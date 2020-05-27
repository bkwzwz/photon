%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Configuration-management, application deployment, cloud provisioning system
Name:           ansible
Version:        2.8.10
Release:        2%{?dist}
License:        GPLv3+
URL:            https://www.ansible.com
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://releases.ansible.com/ansible/%{name}-%{version}.tar.gz
%define sha1 %{name}=4e1e909fb8f01c4327766f8a544362dfa3ca1c4e

Patch0:         ansible-tdnf.patch
Patch1:         CVE-2020-1733.patch
Patch2:         CVE-2020-1735.patch
Patch3:         CVE-2020-1738.patch
Patch4:         CVE-2020-1739.patch
Patch5:         CVE-2020-1740.patch
Patch6:         CVE-2020-10684.patch

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs
Requires:       python-jinja2
Requires:       PyYAML
Requires:       python-xml
Requires:       paramiko
%if %{with_check}
Requires:       python2-devel
%endif

%description
Ansible is a radically simple IT automation system. It handles configuration-management, application deployment, cloud provisioning, ad-hoc task-execution, and multinode orchestration - including trivializing things like zero downtime rolling updates with load balancers.

%prep
%setup -q

%patch0 -p2
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
python2 setup.py build

%install
%{__rm} -rf %{buildroot}
python2 setup.py install -O1 --skip-build \
    --root "%{buildroot}"

%check
python3 setup.py test

%files
%defattr(-, root, root)
%{_bindir}/*
%{python2_sitelib}/*

%changelog
*   Mon Apr 20 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.10-2
-   Fix CVE-2020-1733, CVE-2020-1739
*   Fri Apr 03 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.10-1
-   Upgrade version to 2.8.10 & various CVEs fixed
*   Sun Feb 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.3-3
-   Fix 'make check'
*   Thu Feb 06 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.3-2
-   Fix for CVE-2019-14864
-   Fix dependencies
-   Patch to support tdnf operations
*   Mon Aug 12 2019 Shreenidhi Shedi <sshedi@vmware.com> 2.8.3-1
-   Upgraded to version 2.8.3
*   Tue Jan 22 2019 Anish Swaminathan <anishs@vmware.com> 2.7.6-1
-   Version update to 2.7.6, fix CVE-2018-16876
*   Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 2.6.4-1
-   Version update to 2.6.4
*   Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> 2.4.0.0-1
-   Version update to 2.4.0.0
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.2.2.0-2
-   Use python2 explicitly
*   Thu Apr 6 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.2.0-1
-   Version update
*   Wed Sep 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.1.1.0-1
-   Initial build. First version
