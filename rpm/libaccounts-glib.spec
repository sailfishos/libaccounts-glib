Name: libaccounts-glib
Version: 1.27
Release: 1
License: LGPLv2
Summary: Accounts base library
URL: https://gitlab.com/accounts-sso/libaccounts-glib
Source0: %{name}-%{version}.tar.gz
Patch1: 0001-Compatibility-patch-for-check-0.9.8.patch
Patch2: 0002-Disable-docs.patch
Patch3: 0003-Support-moving-of-database-from-XDG_CONFIG_HOME-to-X.patch
Patch4: 0004-Own-a-bus-name-on-the-dbus-session-bus.patch

BuildRequires:  pkgconfig(check) >= 0.9.4
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(glib-2.0) >= 2.26
BuildRequires:  pkgconfig(gio-2.0) >= 2.30
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(sqlite3) >= 3.7.0
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  libtool
BuildRequires:  meson
BuildRequires:  vala-tools
BuildRequires:  python3-gobject
BuildRequires:  ninja

%description
%{summary}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig(glib-2.0)

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%package tools
Summary:        Tools for %{name}
Requires:       %{name} = %{version}-%{release}

%description tools
This package contains the ag-tool, which can be used to access the accounts DB 
from the command line.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       libtool

%description tests
This package contains tests for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/libaccounts-glib

%build
# not needing the python stuff
%meson \
    -Denable-datadir=true \
    -Ddatabase-dir="system/privileged/Accounts/libaccounts-glib" \
    -Dprivileged-dir="system/privileged"
%meson_build

%install
%meson_install
rm -r %{buildroot}%{_libdir}/girepository-1.0
rm -r %{buildroot}%{_datadir}/dbus-1
rm -r %{buildroot}%{_datadir}/gettext
rm -r %{buildroot}%{_datadir}/gir-1.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libaccounts-glib.so.*
%{_datadir}/xml/accounts/schema/*
%license COPYING

%files devel
%{_includedir}/libaccounts-glib/*.h
%{_libdir}/libaccounts-glib.so
%{_libdir}/pkgconfig/libaccounts-glib.pc
%exclude %{_datadir}/vala

%files tools
%{_bindir}/ag-tool
%{_bindir}/ag-backup
