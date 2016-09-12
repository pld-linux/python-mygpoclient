#
# Conditional build:
%bcond_with	tests	# do not perform "make test"

%define		module		mygpoclient
%define		egg_name	mygpoclient
Summary:	Python module to connect to the my.gpodder.org webservice
Name:		python-%{module}
Version:	1.7
Release:	1
License:	GPL v3+
Group:		Libraries/Python
Source0:	http://thpinfo.com/2010/mygpoclient/mygpoclient-%{version}.tar.gz
# Source0-md5:	fc4e237c40eba0733a362949d304974c
URL:		http://thpinfo.com/2010/mygpoclient/
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%if %{with tests}
BuildRequires:	python-coverage
BuildRequires:	python-minimock
BuildRequires:	python-nose
BuildRequires:	python-simplejson
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
client-library to connect the my.gpodder.org webservice.

%prep
%setup -q -n mygpoclient-%{version}

# Leave out http-tests as they currently fail occasionally (reported upstream)
rm mygpoclient/http_test.py

%build
%py_build

%if %{with tests}
nosetests-%{py_ver} --cover-erase --with-coverage --with-doctest --cover-package=mygpoclient
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install

%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/mygpoclient/*test.py*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README AUTHORS
%attr(755,root,root) %{_bindir}/bpsync
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
