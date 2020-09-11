Name:           libaccounts-glib
Version:        1.24
Release:        1
License:        LGPLv2
Summary:        Accounts base library
URL:            https://gitlab.com/accounts-sso/libaccounts-glib
Source0:        %{name}-%{version}.tar.gz
Source1:        move_accounts_db_to_privileged
Patch0:         0001-Compatibility-patch-for-check-0.9.8.patch
Patch1:         0002-Disable-docs.patch
Patch2:         0003-Avoid-assert-failure-on-ag_provider_get_tags.patch
Patch3:         0004-Support-moving-of-database-from-XDG_CONFIG_HOME-to-X.patch
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
BuildRequires:  oneshot >= 0.6.3
Requires:  oneshot >= 0.6.3
%{_oneshot_requires_post}

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
%meson -Dpy-overrides-dir=/usr/removeme \
    -Denable-datadir=true \
    -Ddatabase-dir="system/privileged/Accounts/libaccounts-glib" \
    -Dprivileged-dir="system/privileged"
%meson_build

%install
%meson_install
rm -r %{buildroot}/usr/removeme
rm -r %{buildroot}%{_libdir}/girepository-1.0
rm -r %{buildroot}%{_datadir}/dbus-1
rm -r %{buildroot}%{_datadir}/gettext
rm -r %{buildroot}%{_datadir}/gir-1.0
mkdir -p %{buildroot}/%{_oneshotdir}
cp -a %SOURCE1 %{buildroot}/%{_oneshotdir}
chmod +x %{buildroot}/%{_oneshotdir}/*

%post
/sbin/ldconfig
if [ "$1" -eq 2 ]; then
# true when run during a package upgrade
%{_bindir}/add-oneshot --late --all-users --privileged move_accounts_db_to_privileged

# add redirect file only if it's needed
USERS=$(getent group users | cut -d ":" -f 4 | tr "," "\n")
for u in $USERS; do
    UHOME=$(getent passwd $u | cut -d: -f6)
    FOLDERBASE=$UHOME/.local/share/system/privileged/Accounts
    FOLDER=$FOLDERBASE/libaccounts-glib
    if [ ! -f "$FOLDER/accounts.db" ]; then
        mkdir -p $FOLDER
        echo "../../../../../../.config/libaccounts-glib" > $FOLDER/accounts.redirect
        chown -R $u:privileged $FOLDERBASE
    fi
done

fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libaccounts-glib.so.*
%{_datadir}/xml/accounts/schema/*
%license COPYING
%{_oneshotdir}/move_accounts_db_to_privileged

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

