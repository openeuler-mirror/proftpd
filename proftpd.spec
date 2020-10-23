%global use_systemd    1
%global rundir        /run
%global rundir_tmpfs    1
%global systemd_units systemd
%global preset_support 1
%global mysql_lib mariadb
%global mysql_devel_pkg mariadb-connector-c-devel
%global postgresql_devel_pkg libpq-devel
%global _hardened_build 1
%undefine _strict_symbol_defs_build
%global rpmrel 20
%global mod_vroot_version 0.9.5
%bcond_with enable_test 0

Name:           proftpd
Version:        1.3.6
Release:        1
Summary:        Flexible, stable and highly-configurable FTP server
License:        GPLv2+
URL:            https://github.com/proftpd/proftpd
Source0:        https://github.com/proftpd/proftpd/archive/v%{version}.tar.gz
Source1:        proftpd.conf
Source5:        proftpd-welcome.msg
Source9:        proftpd.sysconfig
Source10:       http://github.com/Castaglia/proftpd-mod_vroot/archive/v%{mod_vroot_version}.tar.gz
Patch1:         proftpd-1.3.6-shellbang.patch
Patch2:         proftpd.conf-no-memcached.patch
Patch3:         proftpd-1.3.4rc1-mod_vroot-test.patch
# https://github.com/proftpd/proftpd/commit/459693c7.patch
Patch100:       459693c7.patch
# https://github.com/proftpd/proftpd/commit/389cc579.patch
Patch101:       389cc579.patch
# https://github.com/proftpd/proftpd/commit/1825a2b8.patch
Patch102:       1825a2b8.patch
# https://github.com/proftpd/proftpd/commit/73887e02.patch
Patch103:       73887e02.patch
# https://github.com/proftpd/proftpd/commit/8a186e2d.patch
Patch104:       8a186e2d.patch
# https://github.com/proftpd/proftpd/commit/c3e5d75f.patch
Patch105:       c3e5d75f.patch
Patch106:       proftpd-1.3.6-add-enable-tests-nonetwork-option.patch
# https://github.com/proftpd/proftpd/commit/adfdc01d.patch
Patch107:       adfdc01d.patch
# https://github.com/proftpd/proftpd/commit/6cc96b5f.patch
Patch108:       6cc96b5f.patch
# https://github.com/proftpd/proftpd/commit/aa85f127.patch
Patch109:       aa85f127.patch
# https://github.com/proftpd/proftpd/commit/7907aa65.patch
Patch110:       7907aa65.patch
# https://github.com/proftpd/proftpd/commit/08ba2f63.patch
Patch111:       08ba2f63.patch
# https://github.com/proftpd/proftpd/commit/757b9633.patch
Patch112:       757b9633.patch
# https://github.com/proftpd/proftpd/commit/41ecb7dc.patch
Patch113:       41ecb7dc.patch
# https://github.com/proftpd/proftpd/commit/ad786eaa.patch
Patch114:       ad786eaa.patch
# https://github.com/proftpd/proftpd/commit/a2c02a6b.patch
Patch115:       a2c02a6b.patch
Patch116:       proftpd-1.3.6-ENOATTR.patch
# https://github.com/proftpd/proftpd/commit/fa378a8f.patch
Patch117:       fa378a8f.patch
BuildRequires:  coreutils gcc GeoIP-devel gettext libacl-devel libcap-devel
%if 0%{?have_libmemcached:1}
BuildRequires:  libmemcached-devel >= 0.41
%endif
BuildRequires:  %{mysql_devel_pkg} ncurses-devel openldap-devel openssl-devel
BuildRequires:  pam-devel pcre-devel >= 7.0 perl-generators perl-interpreter
BuildRequires:  pkgconfig %{postgresql_devel_pkg} sqlite-devel tar
%if 0%{?libwrap_support:1}
BuildRequires:  tcp_wrappers-devel
%endif
BuildRequires:  zlib-devel
BuildRequires:  check-devel
%if 0%{?_with_integrationtests:1}
BuildRequires:  perl(Compress::Zlib) perl(Digest::MD5) perl(HTTP::Request)
BuildRequires:  perl(IO::Socket::SSL) perl(LWP::UserAgent) perl(Net::FTPSSL)
BuildRequires:  perl(Net::SSLeay) perl(Net::Telnet) perl(Sys::HostAddr) perl(Test::Harness)
BuildRequires:  perl(Test::Unit) >= 0.25 perl(Time::HiRes)
%endif
%if %{rundir_tmpfs}
Requires:       %{systemd_units}
%endif
Requires(preun):coreutils, findutils
%if %{use_systemd}
BuildRequires:  %{systemd_units}
%{?systemd_requires}
%else
Requires(post):  chkconfig
Requires(preun): chkconfig, initscripts
Requires(postun):initscripts
%endif
Provides:        ftpserver
%description
ProFTPD is an enhanced FTP server with a focus toward simplicity, security,
and ease of configuration. It features a very Apache-like configuration
syntax, and a highly customizable server infrastructure, including support for
multiple 'virtual' FTP servers, anonymous FTP, and permission-based directory
visibility.
%if %{use_systemd}
This package defaults to the standalone behavior of ProFTPD, but all the
needed scripts to have it run by systemd instead are included.
%else
This package defaults to the standalone behavior of ProFTPD, but all the
needed scripts to have it run by xinetd instead are included.
%endif

%package     devel
Summary:     ProFTPD - Tools and header files for developers
Requires:    %{name} = %{version}-%{release} gcc libtool GeoIP-devel libacl-devel
Requires:    libcap-devel
%if 0%{?have_libmemcached:1}
Requires:    libmemcached-devel >= 0.41
%endif
Requires:    %{mysql_devel_pkg} ncurses-devel openldap-devel openssl-devel pam-devel
Requires:    pcre-devel pkgconfig %{postgresql_devel_pkg} sqlite-devel
%if 0%{?libwrap_support:1}
Requires:    tcp_wrappers-devel
%endif
Requires:    zlib-devel
%description devel
This package is required to build additional modules for ProFTPD.

%package     ldap
Summary:     Module to add LDAP support to the ProFTPD FTP server
Requires:    %{name} = %{version}-%{release}
%description ldap
Module to add LDAP support to the ProFTPD FTP server.

%package     mysql
Summary:     Module to add MySQL support to the ProFTPD FTP server
Requires:    %{name} = %{version}-%{release}
%description mysql
Module to add MySQL support to the ProFTPD FTP server.

%package     postgresql
Summary:     Module to add PostgreSQL support to the ProFTPD FTP server
Requires:    %{name} = %{version}-%{release}
%description postgresql
Module to add PostgreSQL support to the ProFTPD FTP server.

%package     sqlite
Summary:     Module to add SQLite support to the ProFTPD FTP server
Requires:    %{name} = %{version}-%{release}
%description sqlite
Module to add SQLite support to the ProFTPD FTP server.

%package      utils
Summary:      ProFTPD - Additional utilities
Requires:     %{name} = %{version}-%{release} perl-interpreter
BuildRequires:perl(Crypt::Cracklib)
Requires:     perl(Crypt::Cracklib)
%description  utils
This package contains additional utilities for monitoring and configuring the
ProFTPD server:
* ftpasswd: generate passwd(5) files for use with AuthUserFile
* ftpcount: show the current number of connections per server/virtualhost
* ftpmail: monitor transfer log and send email when files uploaded
* ftpquota: manipulate quota tables
* ftptop: show the current status of FTP sessions
* ftpwho: show the current process information for each FTP session

%prep
%setup -q -n %{name}-%{version}%{?prever}
cd contrib
tar xfz %{SOURCE10}
mv proftpd-mod_vroot-%{mod_vroot_version} mod_vroot
cd -
cp -p %{SOURCE1} proftpd.conf
mv contrib/README contrib/README.contrib
%patch1
%if 0%{!?have_libmemcached:1}
%patch2
%endif
%patch3 -p1 -b .test_vroot
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%if %{use_systemd}
sed -i -e '/killall/s/test.*/systemctl reload proftpd.service/' \
    contrib/dist/rpm/proftpd.logrotate
%endif
chmod -c -x contrib/xferstats.holger-preiss
chmod -c -x include/hanson-tpl.h lib/hanson-tpl.c
find doc/ contrib/ -name '*.orig' -delete

%build
SMOD1=mod_sql:mod_sql_passwd:mod_sql_mysql:mod_sql_postgres:mod_sql_sqlite
SMOD2=mod_quotatab:mod_quotatab_file:mod_quotatab_ldap:mod_quotatab_radius:mod_quotatab_sql
SMOD3=mod_ldap:mod_ban%{?libwrap_support::mod_wrap}:mod_ctrls_admin:mod_facl:mod_load:mod_vroot
SMOD4=mod_radius:mod_ratio:mod_rewrite:mod_site_misc:mod_exec:mod_shaper:mod_geoip
SMOD5=mod_wrap2:mod_wrap2_file:mod_wrap2_sql:mod_copy:mod_deflate:mod_ifversion:mod_qos
SMOD6=mod_sftp:mod_sftp_pam:mod_sftp_sql:mod_tls_shmcache%{?have_libmemcached::mod_tls_memcache}
%configure \
            --libexecdir="%{_libexecdir}/proftpd" \
            --localstatedir="%{rundir}/proftpd" \
            --disable-strip \
            --enable-ctrls \
            --enable-dso \
            --enable-facl \
            --enable-ipv6 \
%{?have_libmemcached:    --enable-memcache} \
            --enable-nls \
            --enable-openssl \
            --disable-pcre \
            --disable-redis \
            --enable-shadow \
            --enable-tests=nonetwork \
            --with-libraries="%{_libdir}/%{mysql_lib}" \
            --with-includes="%{_includedir}/mysql" \
            --with-modules=mod_readme:mod_auth_pam:mod_tls \
            --with-shared=${SMOD1}:${SMOD2}:${SMOD3}:${SMOD4}:${SMOD5}:${SMOD6}:mod_ifsession
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} \
    rundir="%{rundir}/proftpd" \
    INSTALL_USER=`id -un` \
    INSTALL_GROUP=`id -gn`
install -D -p -m 640 proftpd.conf    %{buildroot}%{_sysconfdir}/proftpd.conf
install -D -p -m 644 contrib/dist/rpm/proftpd.pam \
                    %{buildroot}%{_sysconfdir}/pam.d/proftpd
%if %{use_systemd}
install -D -p -m 644 contrib/dist/rpm/proftpd.service \
                    %{buildroot}%{_unitdir}/proftpd.service
install -D -p -m 644 contrib/dist/systemd/proftpd.socket \
                    %{buildroot}%{_unitdir}/proftpd.socket
install -D -p -m 644 contrib/dist/systemd/proftpd@.service \
                    %{buildroot}%{_unitdir}/proftpd@.service
%else
install -D -p -m 755 contrib/dist/rpm/proftpd.init.d \
                    %{buildroot}%{_sysconfdir}/rc.d/init.d/proftpd
install -D -p -m 644 contrib/dist/rpm/xinetd \
                    %{buildroot}%{_sysconfdir}/xinetd.d/xproftpd
%endif
install -D -p -m 644 contrib/dist/rpm/proftpd.logrotate \
                    %{buildroot}%{_sysconfdir}/logrotate.d/proftpd
install -D -p -m 644 %{SOURCE5}        %{buildroot}%{_localstatedir}/ftp/welcome.msg
install -D -p -m 644 %{SOURCE9}        %{buildroot}%{_sysconfdir}/sysconfig/proftpd
mkdir -p %{buildroot}%{_localstatedir}/{ftp/{pub,uploads},log/proftpd}
touch %{buildroot}%{_sysconfdir}/ftpusers
%if %{rundir_tmpfs}
install -d -m 755 %{buildroot}%{_prefix}/lib/tmpfiles.d
install -p -m 644 contrib/dist/rpm/proftpd-tmpfs.conf \
                    %{buildroot}%{_prefix}/lib/tmpfiles.d/proftpd.conf
%endif
%find_lang proftpd

%if %{with enable_test}
%check
%if 0%{?_with_integrationtests:1}
ln ftpdctl tests/
make check
%else
if ! make -C tests api-tests; then
    # Diagnostics to report upstream
    cat tests/api-tests.log
    ./proftpd -V
    # Fail the build
    false
fi
%endif
%endif

%post
%if %{use_systemd}
systemctl daemon-reload &>/dev/null || :
%endif
if [ $1 -eq 1 ]; then
    # Initial installation
%if ! %{use_systemd}
    chkconfig --add proftpd || :
%endif
%if %{preset_support}
    systemctl preset proftpd.service &>/dev/null || :
%endif
    IFS=":"; cat /etc/passwd | \
    while { read username nu nu gid nu nu nu nu; }; do \
        if [ $gid -lt 100 -a "$username" != "ftp" ]; then
            echo $username >> %{_sysconfdir}/ftpusers
        fi
    done
fi

%preun
if [ $1 -eq 0 ]; then
    # Package removal, not upgrade
%if %{use_systemd}
    systemctl --no-reload disable proftpd.service &>/dev/null || :
    systemctl stop proftpd.service &>/dev/null || :
%else
    service proftpd stop &>/dev/null || :
    chkconfig --del proftpd || :
%endif
    find %{rundir}/proftpd -depth -mindepth 1 |
        xargs rm -rf &>/dev/null || :
fi

%postun
%if %{use_systemd}
systemctl daemon-reload &>/dev/null || :
%endif
if [ $1 -ge 1 ]; then
    # Package upgrade, not uninstall
%if %{use_systemd}
    systemctl try-restart proftpd.service &>/dev/null || :
%else
    service proftpd condrestart &>/dev/null || :
else
    # Package removal, not upgrade
    service xinetd reload &>/dev/null || :
%endif
fi

%files -f proftpd.lang
%if 0%{?_licensedir:1}
%license COPYING
%else
%doc COPYING
%endif
%doc CREDITS ChangeLog NEWS README.md
%doc README.DSO README.modules README.IPv6 README.PAM
%doc README.capabilities README.classes README.controls README.facl
%doc contrib/README.contrib contrib/README.ratio
%doc doc/* sample-configurations/
%dir %{_localstatedir}/ftp/
%dir %{_localstatedir}/ftp/pub/
%dir %{rundir}/proftpd/
%config(noreplace) %{_localstatedir}/ftp/welcome.msg
%config(noreplace) %{_sysconfdir}/blacklist.dat
%config(noreplace) %{_sysconfdir}/dhparams.pem
%config(noreplace) %{_sysconfdir}/ftpusers
%config(noreplace) %{_sysconfdir}/logrotate.d/proftpd
%config(noreplace) %{_sysconfdir}/pam.d/proftpd
%config(noreplace) %{_sysconfdir}/proftpd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/proftpd
%if %{use_systemd}
%{_unitdir}/proftpd.service
%{_unitdir}/proftpd.socket
%{_unitdir}/proftpd@.service
%else
%config(noreplace) %{_sysconfdir}/xinetd.d/xproftpd
%{_sysconfdir}/rc.d/init.d/proftpd
%endif
%if %{rundir_tmpfs}
%{_prefix}/lib/tmpfiles.d/proftpd.conf
%endif
%{_bindir}/ftpdctl
%{_sbindir}/ftpscrub
%{_sbindir}/ftpshut
%{_sbindir}/in.proftpd
%{_sbindir}/proftpd
%{_mandir}/man5/proftpd.conf.5*
%{_mandir}/man5/xferlog.5*
%{_mandir}/man8/ftpdctl.8*
%{_mandir}/man8/ftpscrub.8*
%{_mandir}/man8/ftpshut.8*
%{_mandir}/man8/proftpd.8*
%dir %{_libexecdir}/proftpd/
%{_libexecdir}/proftpd/mod_ban.so
%{_libexecdir}/proftpd/mod_ctrls_admin.so
%{_libexecdir}/proftpd/mod_copy.so
%{_libexecdir}/proftpd/mod_deflate.so
%{_libexecdir}/proftpd/mod_exec.so
%{_libexecdir}/proftpd/mod_facl.so
%{_libexecdir}/proftpd/mod_geoip.so
%{_libexecdir}/proftpd/mod_ifsession.so
%{_libexecdir}/proftpd/mod_ifversion.so
%{_libexecdir}/proftpd/mod_load.so
%{_libexecdir}/proftpd/mod_qos.so
%{_libexecdir}/proftpd/mod_quotatab.so
%{_libexecdir}/proftpd/mod_quotatab_file.so
%{_libexecdir}/proftpd/mod_quotatab_radius.so
%{_libexecdir}/proftpd/mod_quotatab_sql.so
%{_libexecdir}/proftpd/mod_radius.so
%{_libexecdir}/proftpd/mod_ratio.so
%{_libexecdir}/proftpd/mod_rewrite.so
%{_libexecdir}/proftpd/mod_sftp.so
%{_libexecdir}/proftpd/mod_sftp_pam.so
%{_libexecdir}/proftpd/mod_sftp_sql.so
%{_libexecdir}/proftpd/mod_shaper.so
%{_libexecdir}/proftpd/mod_site_misc.so
%{_libexecdir}/proftpd/mod_sql.so
%{_libexecdir}/proftpd/mod_sql_passwd.so
%{?have_libmemcached:%{_libexecdir}/proftpd/mod_tls_memcache.so}
%{_libexecdir}/proftpd/mod_tls_shmcache.so
%{_libexecdir}/proftpd/mod_vroot.so
%{?libwrap_support:%{_libexecdir}/proftpd/mod_wrap.so}
%{_libexecdir}/proftpd/mod_wrap2.so
%{_libexecdir}/proftpd/mod_wrap2_file.so
%{_libexecdir}/proftpd/mod_wrap2_sql.so
%exclude %{_libexecdir}/proftpd/*.a
%exclude %{_libexecdir}/proftpd/*.la
%attr(331, ftp, ftp) %dir %{_localstatedir}/ftp/uploads/
%attr(750, root, root) %dir %{_localstatedir}/log/proftpd/

%files devel
%{_bindir}/prxs
%{_includedir}/proftpd/
%{_libdir}/pkgconfig/proftpd.pc

%files ldap
%doc README.LDAP contrib/mod_quotatab_ldap.ldif contrib/mod_quotatab_ldap.schema
%{_libexecdir}/proftpd/mod_ldap.so
%{_libexecdir}/proftpd/mod_quotatab_ldap.so

%files mysql
%{_libexecdir}/proftpd/mod_sql_mysql.so

%files postgresql
%{_libexecdir}/proftpd/mod_sql_postgres.so

%files sqlite
%{_libexecdir}/proftpd/mod_sql_sqlite.so

%files utils
%doc contrib/xferstats.holger-preiss
%{_bindir}/ftpasswd
%{_bindir}/ftpcount
%{_bindir}/ftpmail
%{_bindir}/ftpquota
%{_bindir}/ftptop
%{_bindir}/ftpwho
%{_mandir}/man1/ftpasswd.1*
%{_mandir}/man1/ftpcount.1*
%{_mandir}/man1/ftpmail.1*
%{_mandir}/man1/ftpquota.1*
%{_mandir}/man1/ftptop.1*
%{_mandir}/man1/ftpwho.1*

%changelog
* Wed Oct 14 2020 chengzihan <chengzihan2@huawei.com> - 1.3.6-1
- Package init
