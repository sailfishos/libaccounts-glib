Name:           libaccounts-glib
Version:        1.18
Release:        1
License:        LGPLv2.1
Summary:        Accounts base library
URL:            https://gitlab.com/accounts-sso/libaccounts-glib
Group:          System/Libraries
Source:         %{name}-%{version}.tar.gz
Patch0:         0001-Remove-gtk-doc-dependency-for-disable-gtk-doc.patch
Patch1:         0002-Allow-deprecation-warnings.patch
Patch2:         0003-Remove-use-of-function-only-available-in-check-0.9.1.patch
Patch3:         0004-Add-test-directory-path-for-test-script.patch
Patch4:         0005-Remove-usages-of-ck_assert_uint_eq-from-unit-test.patch
BuildRequires:  pkgconfig(check) >= 0.9.4
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(glib-2.0) >= 2.26
BuildRequires:  pkgconfig(gio-2.0) >= 2.30
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(sqlite3) >= 3.7.0
BuildRequires:  libtool

%description
%{summary}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig(glib-2.0)

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%package tools
Summary:        Tools for %{name}
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description tools
This package contains the ag-tool, which can be used to access the accounts DB 
from the command line.

%package tests
Summary:        Tests for %{name}
Group:          System/X11
Requires:       %{name} = %{version}-%{release}
Requires:       libtool

%description tests
This package contains tests for %{name}.

%prep
%setup -q -n %{name}-%{version}/libaccounts-glib
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
export SERVICE_FILES_DIR=/usr/share/accounts/services
export SERVICE_TYPE_FILES_DIR=/usr/share/accounts/service-types 
export PROVIDER_FILES_DIR=/usr/share/accounts/providers 
%autogen --disable-static \
         --disable-gtk-doc \
         --disable-man \
         --with-testdir=/opt/tests/libaccounts-glib \
         --with-testdatadir=/opt/tests/libaccounts-glib/data
make %{?_smp_mflags}

%install
%make_install
rm  %{buildroot}%{_datadir}/dbus-1/interfaces/com.google.code.AccountsSSO.Accounts.Manager.xml

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libaccounts-glib.so.*
%{_datadir}/backup-framework/applications/accounts.conf
%{_datadir}/xml/accounts/schema/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libaccounts-glib/*.h
%{_libdir}/libaccounts-glib.so
%{_libdir}/pkgconfig/libaccounts-glib.pc
%exclude %{_datadir}/vala

%files tools
%defattr(-,root,root,-)
%{_bindir}/ag-tool
%{_bindir}/ag-backup

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}
