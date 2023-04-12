# With systemd, the runtime directory is /run on tmpfs rather than /var/run on persistent storage
%global use_systemd	1
%global rundir		/run
%global rundir_tmpfs	1

%global systemd_units systemd

%global preset_support 1

%global mysql_lib mariadb
%global mysql_devel_pkg mariadb-connector-c-devel

# Do a hardened build where possible
%global _hardened_build 1

# Dynamic modules contain references to symbols in main daemon, so we need to disable linker checks for undefined symbols
%undefine _strict_symbol_defs_build

%global mod_vroot_version 0.9.11

%global vendor %{?_vendor:%{_vendor}}%{!?_vendor:openEuler}

Name:			proftpd
Version:		1.3.8
Release:		1
Summary:		Flexible, stable and highly-configurable FTP server
License:		GPLv2+
URL:			http://www.proftpd.org/

Source0:		https://github.com/proftpd/proftpd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:		proftpd.conf
Source2:		modules.conf
Source3:		mod_tls.conf
Source4:		mod_ban.conf
Source5:		mod_qos.conf
Source6:		anonftp.conf
Source8:		proftpd-welcome.msg
Source9:		proftpd.sysconfig
Source10:		http://github.com/Castaglia/proftpd-mod_vroot/archive/v%{mod_vroot_version}.tar.gz

Patch1:			proftpd-1.3.8-shellbang.patch
Patch2:			proftpd.conf-no-memcached.patch
Patch3:			proftpd-1.3.4rc1-mod_vroot-test.patch
Patch4:			proftpd-1.3.6-no-mod-wrap.patch
Patch5:			proftpd-1.3.6-no-mod-geoip.patch
Patch6:			proftpd-1.3.7rc3-logging-not-systemd.patch
Patch8:			proftpd-1.3.8-fix-environment-sensitive-tests-failure.patch
Patch9:			1592.patch

BuildRequires:		coreutils
BuildRequires:		gcc
BuildRequires:		gettext
BuildRequires:		libacl-devel
BuildRequires:		libcap-devel
BuildRequires:		logrotate
BuildRequires:		%{mysql_devel_pkg}
BuildRequires:		ncurses-devel
BuildRequires:		openldap-devel
BuildRequires:		openssl-devel
BuildRequires:		pam-devel
BuildRequires:		pcre-devel >= 7.0
BuildRequires:		perl-generators
BuildRequires:		perl-interpreter
BuildRequires:		pkgconfig
%if %{?vendor:1}0
BuildRequires:		postgresql-devel
%endif
BuildRequires:		sed
BuildRequires:		sqlite-devel
BuildRequires:		tar
BuildRequires:		zlib-devel
BuildRequires:		chrpath
BuildRequires:		libidn2-devel
BuildRequires:		libmemcached-devel >= 0.41
BuildRequires:		pcre2-devel >= 10.30
BuildRequires:		tcp_wrappers-devel

# Test suite requirements
BuildRequires:		check-devel
%if 0%{?_with_integrationtests:1}
BuildRequires:		perl(Compress::Zlib)
BuildRequires:		perl(Digest::MD5)
BuildRequires:		perl(HTTP::Request)
BuildRequires:		perl(IO::Socket::SSL)
BuildRequires:		perl(LWP::UserAgent)
BuildRequires:		perl(Net::FTPSSL)
BuildRequires:		perl(Net::SSLeay)
BuildRequires:		perl(Net::Telnet)
BuildRequires:		perl(Sys::HostAddr)
BuildRequires:		perl(Test::Harness)
BuildRequires:		perl(Test::Unit) >= 0.25
BuildRequires:		perl(Time::HiRes)
%endif

# Need %%{systemd_units} for ownership of /usr/lib/tmpfiles.d directory
%if %{rundir_tmpfs}
Requires:		%{systemd_units}
%endif

# Logs should be rotated periodically
Requires:		logrotate

# Scriptlet dependencies
Requires(preun):	coreutils, findutils
%if %{use_systemd}
BuildRequires:		%{systemd_units}
%{?systemd_requires}
%else
Requires(post):		chkconfig
Requires(preun):	chkconfig, initscripts
Requires(postun):	initscripts
%endif

Provides:		ftpserver

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

%package devel
Summary:	ProFTPD - Tools and header files for developers
Requires:	%{name} = %{version}-%{release}
# devel package requires the same devel packages as were build-required
# for the main package
Requires:	gcc, libtool
Requires:	libacl-devel
Requires:	libcap-devel
Requires:	%{mysql_devel_pkg}
Requires:	ncurses-devel
Requires:	openldap-devel
Requires:	openssl-devel
Requires:	pam-devel
Requires:	pcre-devel
Requires:	pkgconfig
%if %{?vendor:1}0
Requires:	postgresql-devel
%endif
Requires:	sqlite-devel
Requires:	zlib-devel
Requires:	libmemcached-devel >= 0.41
Requires:	pcre2-devel >= 10.30
Requires:	tcp_wrappers-devel


%description devel
This package is required to build additional modules for ProFTPD.

%package ldap
Summary:	Module to add LDAP support to the ProFTPD FTP server
Requires:	%{name} = %{version}-%{release}

%description ldap
Module to add LDAP support to the ProFTPD FTP server.

%package mysql
Summary:	Module to add MySQL support to the ProFTPD FTP server
Requires:	%{name} = %{version}-%{release}

%description mysql
Module to add MySQL support to the ProFTPD FTP server.

%if %{?vendor:1}0
%package postgresql
Summary:	Module to add PostgreSQL support to the ProFTPD FTP server
Requires:	%{name} = %{version}-%{release}

%description postgresql
Module to add PostgreSQL support to the ProFTPD FTP server.
%endif

%package sqlite
Summary:	Module to add SQLite support to the ProFTPD FTP server
Requires:	%{name} = %{version}-%{release}

%description sqlite
Module to add SQLite support to the ProFTPD FTP server.

%package utils
Summary:	ProFTPD - Additional utilities
Requires:	%{name} = %{version}-%{release}
Requires:	perl-interpreter

BuildRequires:	perl(Crypt::Cracklib)
Requires:	perl(Crypt::Cracklib)

%description utils
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

# Extract mod_vroot source into contrib/
# Directory must be named mod_vroot for configure script to find it
cd contrib
tar xfz %{SOURCE10}
mv proftpd-mod_vroot-%{mod_vroot_version} mod_vroot
cd -

# Default config files
sed -e 's|@RUNDIR@|%{rundir}|' %{SOURCE1} > proftpd.conf
sed -e 's|@RUNDIR@|%{rundir}|' %{SOURCE2} > modules.conf
sed -e 's|@RUNDIR@|%{rundir}|' %{SOURCE3} > mod_tls.conf
sed -e 's|@RUNDIR@|%{rundir}|' %{SOURCE4} > mod_ban.conf
sed -e 's|@RUNDIR@|%{rundir}|' %{SOURCE5} > mod_qos.conf
sed -e 's|@RUNDIR@|%{rundir}|' %{SOURCE6} > anonftp.conf

# Avoid documentation name conflicts
mv contrib/README contrib/README.contrib

# Change shellbangs /usr/bin/env perl ⇒ /usr/bin/perl
%patch1

# If we don't have libmemcached support, remove the mod_tls_memcache
# snippet from the config file
%patch2

# If we're running the full test suite, include the mod_vroot test
%patch3 -p1 -b .test_vroot

# Remove references to mod_wrap from the configuration file if necessary
%patch4 -b .nowrappers

# Remove references to mod_geoip from the configuration file if necessary
%patch5 -b .nogeoip

%if %{use_systemd}
# Tweak logrotate script for systemd compatibility (#802178)
sed -i -e '/killall/s/test.*/systemctl reload proftpd.service/' \
	contrib/dist/rpm/proftpd.logrotate
%else
# Not using systemd, so we want hostname and timestamp in log messages
%patch6
%endif

%patch8 -p1

%patch9 -p1 -b .libidn2

# Avoid docfile dependencies
chmod -c -x contrib/xferstats.holger-preiss

# Remove bogus exec permissions from source files
chmod -c -x include/hanson-tpl.h lib/hanson-tpl.c

# Remove any patch backup files from documentation
find doc/ contrib/ -name '*.orig' -delete

%build
# Modules to be built as DSO's (excluding mod_ifsession, always specified last)
%if %{?vendor:1}0
SMOD1=mod_sql:mod_sql_passwd:mod_sql_mysql:mod_sql_postgres:mod_sql_sqlite
%else
SMOD1=mod_sql:mod_sql_passwd:mod_sql_mysql:mod_sql_sqlite
%endif
SMOD2=mod_quotatab:mod_quotatab_file:mod_quotatab_ldap:mod_quotatab_radius:mod_quotatab_sql
SMOD3=mod_ldap:mod_ban:mod_ctrls_admin:mod_facl:mod_load:mod_vroot
SMOD4=mod_radius:mod_ratio:mod_rewrite:mod_site_misc:mod_exec:mod_shaper
SMOD5=mod_wrap2:mod_wrap2_file:mod_wrap2_sql:mod_copy:mod_deflate:mod_ifversion:mod_qos
SMOD6=mod_sftp:mod_sftp_pam:mod_sftp_sql:mod_tls_shmcache
SMOD7=mod_unique_id

%configure \
			--libexecdir="%{_libexecdir}/proftpd" \
			--localstatedir="%{rundir}/proftpd" \
			--disable-strip \
			--enable-memcache \
			--enable-pcre2 \
			--enable-ctrls \
			--enable-dso \
			--enable-facl \
			--enable-ipv6 \
			--enable-nls \
			--enable-openssl \
			--disable-pcre \
			--disable-redis \
			--enable-shadow \
			--enable-tests=nonetwork \
			--with-libraries="%{_libdir}/%{mysql_lib}" \
			--with-includes="%{_includedir}/mysql" \
			--with-modules=mod_readme:mod_auth_pam:mod_tls \
			--with-shared=${SMOD1}:${SMOD2}:${SMOD3}:${SMOD4}:${SMOD5}:${SMOD6}:${SMOD7}:mod_ifsession
%make_build

%install
%{make_install} INSTALL_USER=`id -un` INSTALL_GROUP=`id -gn`
mkdir -p %{buildroot}%{_sysconfdir}/proftpd/conf.d
install -D -p -m 640 proftpd.conf	%{buildroot}%{_sysconfdir}/proftpd.conf
install -D -p -m 640 anonftp.conf	%{buildroot}%{_sysconfdir}/proftpd/anonftp.conf
install -D -p -m 640 modules.conf	%{buildroot}%{_sysconfdir}/proftpd/modules.conf
install -D -p -m 640 mod_ban.conf	%{buildroot}%{_sysconfdir}/proftpd/mod_ban.conf
install -D -p -m 640 mod_qos.conf	%{buildroot}%{_sysconfdir}/proftpd/mod_qos.conf
install -D -p -m 640 mod_tls.conf	%{buildroot}%{_sysconfdir}/proftpd/mod_tls.conf
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
install -D -p -m 644 %{SOURCE8}		%{buildroot}%{_localstatedir}/ftp/welcome.msg
install -D -p -m 644 %{SOURCE9}		%{buildroot}%{_sysconfdir}/sysconfig/proftpd
mkdir -p %{buildroot}%{_localstatedir}/{ftp/{pub,uploads},log/proftpd}
touch %{buildroot}%{_sysconfdir}/ftpusers

# Make sure %%{rundir}/proftpd exists at boot time for systems where it's on tmpfs (#656675)
%if %{rundir_tmpfs}
install -d -m 755 %{buildroot}%{_prefix}/lib/tmpfiles.d
install -p -m 644 contrib/dist/rpm/proftpd-tmpfs.conf \
					%{buildroot}%{_prefix}/lib/tmpfiles.d/proftpd.conf
%endif

chrpath -d %{buildroot}%{_sbindir}/proftpd

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

# Find translations
%find_lang proftpd

%check
# Integration tests not fully maintained - stick to API tests only by default
%if 0%{?_with_integrationtests:1}
ln ftpdctl tests/
make check
%else
#API tests should always be OK
export HOSTNAME=`cat /etc/hosts | grep 127.0.0.1 | head -1| awk '{print $2}'`
if ! make -C tests api-tests; then
	# Diagnostics to report upstream
	cat tests/api-tests.log
	./proftpd -V
	# Fail the build
	false
fi
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
/sbin/ldconfig

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
/sbin/ldconfig

%files -f proftpd.lang
%if 0%{?_licensedir:1}
%license COPYING
%else
%doc COPYING
%endif
%doc CREDITS ChangeLog NEWS README.md
%doc README.modules contrib/README.contrib contrib/README.ratio
%doc doc/* sample-configurations/
%dir %{_localstatedir}/ftp/
%dir %{_localstatedir}/ftp/pub/
%dir %{rundir}/proftpd/
%dir %{_sysconfdir}/logrotate.d/
%dir %{_sysconfdir}/proftpd/
%dir %{_sysconfdir}/proftpd/conf.d/
%config(noreplace) %{_localstatedir}/ftp/welcome.msg
%config(noreplace) %{_sysconfdir}/blacklist.dat
%config(noreplace) %{_sysconfdir}/dhparams.pem
%config(noreplace) %{_sysconfdir}/ftpusers
%config(noreplace) %{_sysconfdir}/logrotate.d/proftpd
%config(noreplace) %{_sysconfdir}/pam.d/proftpd
%config(noreplace) %{_sysconfdir}/proftpd.conf
%config(noreplace) %{_sysconfdir}/proftpd/anonftp.conf
%config(noreplace) %{_sysconfdir}/proftpd/modules.conf
%config(noreplace) %{_sysconfdir}/proftpd/mod_ban.conf
%config(noreplace) %{_sysconfdir}/proftpd/mod_qos.conf
%config(noreplace) %{_sysconfdir}/proftpd/mod_tls.conf
%config(noreplace) %{_sysconfdir}/sysconfig/proftpd
%config(noreplace) /etc/ld.so.conf.d/*
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
%{_libexecdir}/proftpd/mod_ifsession.so
%{_libexecdir}/proftpd/mod_ifversion.so
%{_libexecdir}/proftpd/mod_unique_id.so
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
%{_libexecdir}/proftpd/mod_tls_shmcache.so
%{_libexecdir}/proftpd/mod_vroot.so
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

%if %{?vendor:1}0
%files postgresql
%{_libexecdir}/proftpd/mod_sql_postgres.so
%endif

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
* Tue Apr 11 2023 chenchen <chen_aka_jan@163.com> - 1.3.8-1
- Update to 1.3.8

* Fri Nov 18 2022 caodongxia <caodongxia@h-partners.com> - 1.3.7c-4
- Replace openEuler with vendor macro

* Thu Mar 17 2022 gaihuiying <eaglegai@163.com> - 1.3.7c-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add macro to control if postgresql is need

* Fri Jan 07 2022 gaihuiying <gaihuiying1@huawei.com> - 1.3.7c-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix environment sensitive tests failure

* Sat Dec 04 2021 quanhongfei <quanhongfei@huawei.com> - 1.3.7c-1
- Type:requirement
- ID:NA
- SUG:NA
- DESC:update proftpd to 1.3.7c

* Tue Sep 07 2021 gaihuiying <gaihuiying1@huawei.com> - 1.3.7a-2
- Type:requirement
- ID:NA
- SUG:NA
- DESC:remove rpath of proftpd

* Tue Jun 1 2021 gaihuiying <gaihuiying1@huawei.com> - 1.3.7a-1
- Update to 1.3.7a

* Wed Oct 14 2020 chengzihan <chengzihan2@huawei.com> - 1.3.6-1
- Package init
