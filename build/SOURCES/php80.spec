# with backport stuff, adapted from
#
# Fedora spec file for php
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
# API/ABI check
%global apiver      20200930
%global zendver     20200930
%global pdover      20170320
# Extension version
%global fileinfover 1.0.5
%global oci8ver     3.0.1
%global zipver      1.19.5

# Adds -z now to the linker flags
%global _hardened_build 1

# version used for php embedded library soname
%global embed_version 8.0

%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

%global oraclever 23.26.3
%global oraclemax 24
%global oraclelib 23.1
%global oracledir 23

# Build for LiteSpeed Web Server (LSAPI), you can disable using --without tests
%bcond_without        lsws

# Regression tests take a long time, you can skip 'em using --without tests
%bcond_without        tests

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%global mysql_config %{_libdir}/mysql/mysql_config

# Optional Oracle extensions; pass "--with oci8" etc to rpmbuild.
%bcond_with           oci8

%bcond_without        imap

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
# switch to bundled library using --without libpcre
%bcond_without        libpcre
%else
# switch to system library using --with libpcre
%bcond_with           libpcre
%endif

# Using qdbm from "remi" for now, see https://bugzilla.redhat.com/2017308
%if 0%{?fedora} >= 33 || 0%{?rhel} >= 8
%bcond_without        qdbm
%else
%bcond_with           qdbm
%endif

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 8
# switch to bundled library using --without libxcrypt
%bcond_without        libxcrypt
%else
# switch to system library using --with libxcrypt
%bcond_with           libxcrypt
%endif

# Build firebird extensions, you can disable using --without firebird
%if 0%{?rhel} > 10
%bcond_with           firebird
%else
%bcond_without        firebird
%endif

# Build ZTS extension or only NTS using --without zts
%ifarch x86_64
%bcond_without        zts
%else
%bcond_with           zts
%endif

# Debug build, using --with debug
%bcond_with           debug

# /usr/sbin/apsx with httpd < 2.4 and defined as /usr/bin/apxs with httpd >= 2.4
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:     %{expand: %%global _httpd_moddir     %%{_libdir}/httpd/modules}}
%{!?_httpd_contentdir: %{expand: %%global _httpd_contentdir /var/www}}

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# httpd 2.4.10 with httpd-filesystem and sethandler support
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 8
%global with_httpd2410 1
%else
%global with_httpd2410 0
%endif
# nginx 1.6 with nginx-filesystem
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 8
%global with_nginx     1
%else
%global with_nginx     0
%endif

%bcond_without         dtrace
%bcond_without         libgd
%bcond_with            zip

%global upver          8.0.30

Summary: PHP scripting language for creating dynamic web sites
Name: php
Version: %{upver}%{?rcver:~%{rcver}}
Release: 21%{?dist}
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
# ext/date/lib is MIT
# Zend/zend_sort is NCSA
License: PHP and Zend and BSD and MIT and ASL 1.0 and NCSA
URL: http://www.php.net/

Source0: http://www.php.net/distributions/php-%{upver}%{?rcver}.tar.xz
Source1: php.conf
Source2: php.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.service
Source7: php-fpm.logrotate
Source8: php-fpm.sysconfig
Source9: php.modconf
Source11: php.conf2
Source12: php-fpm.wants
Source13: nginx-fpm.conf
Source14: nginx-php.conf
# See https://secure.php.net/gpg-keys.php
Source20: https://www.php.net/distributions/php-keyring.gpg
Source21: https://www.php.net/distributions/php-%{upver}%{?rcver}.tar.xz.asc
# Configuration files for some extensions
Source50: 10-opcache.ini
Source51: opcache-default.blacklist
Source52: 20-oci8.ini
Source53: 20-ffi.ini

# Build fixes
Patch1: php-7.4.0-httpd.patch
Patch5: php-7.2.0-includedir.patch
Patch6: php-8.0.0-embed.patch
Patch7: php-7.4.0-libdb.patch
# get rid of deprecated functions from 8.1
Patch9: php-8.0.6-deprecated.patch
# For recent ICU from 8.2
Patch11: php-8.0.30-icu.patch
# Fix strict prototypes from 8.1
Patch12: php-8.0.30-proto.patch
# Fix for bash 5.3 (Fedora 43)
Patch13: php-7.4.33-bash53.patch

# Functional changes
# Use system nikic/php-parser
Patch41: php-8.0.19-parser.patch
# use system tzdata
Patch42: php-8.0.10-systzdata-v21.patch
# See http://bugs.php.net/53436
Patch43: php-7.4.0-phpize.patch
# Use -lldap_r for OpenLDAP
Patch45: php-7.4.0-ldap_r.patch
# Ignore unsupported "threads" option on password_hash
Patch46: php-8.0.7-argon2.patch
# drop "Configure command" from phpinfo output
# and only use gcc (instead of full version)
Patch47: php-8.0.0-phpinfo.patch
# add sha256 / sha512 security protocol, from 8.1
Patch48: php-8.0.10-snmp-sha.patch
# switch phar to use sha256 signature by default, from 8.1
# implement openssl_256 and openssl_512 for phar signatures, from 8.1
Patch49: php-8.0.10-phar-sha.patch
# compatibility with OpenSSL 3.0, from 8.1
Patch50: php-8.0.21-openssl3.patch
# use system libxcrypt, from 8.1
Patch51: php-8.0.13-crypt.patch
# display TZData version for intl
Patch52: php-8.0.28-intlinfo.patch

# RC Patch
Patch91: php-7.2.0-oci8conf.patch

# Upstream fixes (100+)

# Security fixes (200+)
Patch200: php-cve-2024-2756.patch
Patch201: php-cve-2024-3096.patch
Patch202: php-cve-2024-5458.patch
Patch203: php-cve-2024-8925.patch
Patch204: php-cve-2024-8926.patch
Patch205: php-cve-2024-8927.patch
Patch206: php-cve-2024-9026.patch
Patch207: php-cve-2024-11236.patch
Patch208: php-cve-2024-11234.patch
Patch209: php-cve-2024-8932.patch
Patch210: php-cve-2024-11233.patch
Patch211: php-ghsa-4w77-75f9-2c8w.patch
Patch212: php-cve-2024-8929.patch
Patch213: php-cve-2025-1217.patch
Patch214: php-cve-2025-1734.patch
Patch215: php-cve-2025-1861.patch
Patch216: php-cve-2025-1736.patch
Patch217: php-cve-2025-1219.patch
Patch218: php-cve-2025-6491.patch
Patch219: php-cve-2025-1220.patch
Patch220: php-cve-2025-1735.patch
Patch221: php-cve-2025-14177.patch
Patch222: php-cve-2025-14178.patch
Patch223: php-ghsa-www2-q4fc-65wf.patch
Patch224: php-cve-2025-14179.patch
Patch225: php-cve-2026-6722.patch
Patch226: php-cve-2026-7261.patch
Patch227: php-cve-2026-7262.patch
Patch228: php-cve-2026-6735.patch
Patch229: php-cve-2026-7259.patch
Patch230: php-cve-2026-7568.patch
Patch231: php-cve-2026-7258.patch
# From 8.2.32
Patch232: php-cve-2026-14355.patch
# From 8.2.33
Patch233: php-cve-2026-9672.patch
Patch234: php-cve-2026-17543.patch
Patch235: php-cve-2026-7260.patch
Patch236: php-gh22643.patch
# One cumulative patch per version
Patch237: php-from-8.2.34-to-8.0.patch
Patch238: php-from-8.2.35-to-8.0.patch

# Fixes for tests (300+)
# Factory is droped from system tzdata
Patch300: php-7.4.0-datetests.patch
Patch301: php-8.0.30-zlib-tests.patch
Patch302: php-8.0.30-pcretests.patch

# WIP

BuildRequires: gnupg2
BuildRequires: bzip2-devel
BuildRequires: pkgconfig(libcurl)  >= 7.29.0
BuildRequires: httpd-devel >= 2.0.46-1
BuildRequires: pam-devel
%if %{with_httpd2410}
# to ensure we are using httpd with filesystem feature (see #1081453)
BuildRequires: httpd-filesystem
%endif
%if %{with_nginx}
# to ensure we are using nginx with filesystem feature (see #1142298)
BuildRequires: nginx-filesystem
%endif
BuildRequires: %{?dtsprefix}libstdc++-devel
# no pkgconfig to avoid compat-openssl10
BuildRequires: openssl-devel >= 1.0.1
BuildRequires: pkgconfig(sqlite3) >= 3.7.4
BuildRequires: pkgconfig(zlib) >= 1.2.0.4
BuildRequires: smtpdaemon
BuildRequires: pkgconfig(libedit)
%if %{with libpcre}
BuildRequires: pkgconfig(libpcre2-8) >= 10.30
%else
Provides:      bundled(pcre2) = 10.35
%endif
%if %{with libxcrypt}
BuildRequires: pkgconfig(libxcrypt)
%endif
BuildRequires: bzip2
BuildRequires: perl
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: make
BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?dtsprefix}gcc-c++
BuildRequires: libtool
BuildRequires: libtool-ltdl-devel
%if %{with dtrace}
BuildRequires: %{?dtsprefix}systemtap-sdt-devel
%if 0%{?fedora} >= 41
BuildRequires: %{?dtsprefix}systemtap-sdt-dtrace
%endif
%endif
#BuildRequires: bison
#BuildRequires: re2c
# used for tests
BuildRequires: /bin/ps

%if 0%{?rhel} == 7
Obsoletes: php53, php53u, php54, php54w, php55u, php55w, php56u, php56w, mod_php70u, php70w, mod_php71u, mod_php71w, mod_php72u, mod_php72w
Obsoletes: mod_php73, mod_php73w
Obsoletes: mod_php74, mod_php74w
Obsoletes: mod_php80
%endif
%if %{with zts}
Obsoletes: php-zts < 5.3.7
Provides: php-zts = %{version}-%{release}
Provides: php-zts%{?_isa} = %{version}-%{release}
%endif

Requires: httpd-mmn = %{_httpd_mmn}
Provides: mod_php = %{version}-%{release}
Requires: php-common%{?_isa} = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:
%if %{with_httpd2410}
Requires(pre): httpd-filesystem
%else
Requires(pre): httpd
%endif
# php engine for Apache httpd webserver
Provides: php(httpd)
%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
# For backwards-compatibility, require php-cli for the time being:
Recommends: php-cli%{?_isa}      = %{version}-%{release}
# httpd have threaded MPM by default
Recommends: php-fpm%{?_isa}      = %{version}-%{release}
# as "php" is now mostly a meta-package, commonly used extensions
Recommends: php-mbstring%{?_isa} = %{version}-%{release}
Recommends: php-opcache%{?_isa}  = %{version}-%{release}
Recommends: php-pdo%{?_isa}      = %{version}-%{release}
Recommends: php-sodium%{?_isa}   = %{version}-%{release}
Recommends: php-xml%{?_isa}      = %{version}-%{release}
%else
# For backwards-compatibility, require php-cli for the time being:
Requires:   php-cli%{?_isa}      = %{version}-%{release}
# For ARGON2 password
Requires:   php-sodium%{?_isa}   = %{version}-%{release}
%endif


%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The php package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

%package cli
Summary: Command-line interface for PHP
# sapi/cli/ps_title.c is PostgreSQL
License:  PHP and Zend and BSD and MIT and ASL 1.0 and NCSA and PostgreSQL
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-cgi = %{version}-%{release}, php-cgi%{?_isa} = %{version}-%{release}
Provides: php-pcntl, php-pcntl%{?_isa}
Provides: php-readline, php-readline%{?_isa}
%if 0%{?rhel} == 7
Obsoletes: php53-cli, php53u-cli, php54-cli, php54w-cli, php55u-cli, php55w-cli, php56u-cli, php56w-cli
Obsoletes: php70u-cli, php70w-cli, php71u-cli, php71w-cli, php72u-cli, php72w-cli
Obsoletes: php73-cli, php73w-cli
Obsoletes: php74-cli, php74w-cli
Obsoletes: php80-cli
%endif

%description cli
The php-cli package contains the command-line interface
executing PHP scripts, /usr/bin/php, and the CGI interface.


%package dbg
Summary: The interactive PHP debugger
Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel} == 7
Obsoletes: php56u-dbg, php56w-phpdbg, php70u-dbg, php70w-phpdbg, php71u-dbg, php71w-phpdbg, php72u-dbg, php72w-phpdbg
Obsoletes: php73-dbg, php73w-phpdbg
Obsoletes: php74-dbg, php74w-phpdbg
Obsoletes: php80-dbg
%endif
%description dbg
The php-dbg package contains the interactive PHP debugger.


%package fpm
Summary: PHP FastCGI Process Manager
BuildRequires: libacl-devel
BuildRequires: pkgconfig(libsystemd) >= 209
Requires: php-common%{?_isa} = %{version}-%{release}
%{?systemd_requires}
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
Requires(post): systemd-sysv
%if %{with_httpd2410}
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd-filesystem
# For php.conf in /etc/httpd/conf.d
# and version 2.4.10 for proxy support in SetHandler
Requires: httpd-filesystem >= 2.4.10
# php engine for Apache httpd webserver
Provides: php(httpd)
%else
Requires(pre): /usr/sbin/useradd
%endif
%if %{with_nginx}
# for /etc/nginx ownership
# Temporarily not mandatory to allow nginx for nginx repo
Recommends: nginx-filesystem
%endif
%if 0%{?rhel} == 7
Obsoletes: php53-fpm, php53u-fpm, php54-fpm, php54w-fpm, php55u-fpm, php55w-fpm, php56u-fpm, php56w-fpm
Obsoletes: php70u-fpm, php70w-fpm, php71u-fpm, php71w-fpm, php72u-fpm, php72w-fpm
Obsoletes: php73-fpm, php73w-fpm
Obsoletes: php74-fpm, php74w-fpm
Obsoletes: php80-fpm
%endif

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.

%if %{with lsws}
%package litespeed
Summary: LiteSpeed Web Server PHP support
Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel} == 7
Obsoletes: php53-litespeed, php53u-litespeed, php54-litespeed, php54w-litespeed, php55u-litespeed, php55w-litespeed, php56u-litespeed, php56w-litespeed
Obsoletes: php70u-litespeed, php70w-litespeed, php71u-litespeed, php71w-litespeed, php72u-litespeed, php72w-litespeed
Obsoletes: php73-litespeed, php73w-litespeed
Obsoletes: php74-litespeed, php74w-litespeed
Obsoletes: php80-litespeed
%endif

%description litespeed
The php-litespeed package provides the %{_bindir}/lsphp command
used by the LiteSpeed Web Server (LSAPI enabled PHP).
%endif

%package common
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic are licensed under BSD
License: PHP and BSD

Requires:  tzdata
%if %{with libpcre}
%global pcre2_buildver %(pkg-config --silence-errors --modversion libpcre2-8 2>/dev/null || echo 10.30)
Requires:  pcre2%{?_isa} >= %{pcre2_buildver}
%endif

# ABI/API check - Arch specific
Provides: php(api) = %{apiver}-%{__isa_bits}
Provides: php(zend-abi) = %{zendver}-%{__isa_bits}
Provides: php(language) = %{version}, php(language)%{?_isa} = %{version}
# Provides for all builtin/shared modules:
Provides: php-bz2, php-bz2%{?_isa}
Provides: php-calendar, php-calendar%{?_isa}
Provides: php-core = %{version}, php-core%{?_isa} = %{version}
Provides: php-ctype, php-ctype%{?_isa}
Provides: php-curl, php-curl%{?_isa}
Provides: php-date, php-date%{?_isa}
Provides: bundled(timelib)
Provides: php-exif, php-exif%{?_isa}
Provides: php-fileinfo, php-fileinfo%{?_isa}
Provides: bundled(libmagic) = 5.29
Provides: php-filter, php-filter%{?_isa}
Provides: php-ftp, php-ftp%{?_isa}
Provides: php-gettext, php-gettext%{?_isa}
Provides: php-hash, php-hash%{?_isa}
Provides: php-mhash = %{version}, php-mhash%{?_isa} = %{version}
Provides: php-iconv, php-iconv%{?_isa}
Obsoletes: php-json < 8
Obsoletes: php-pecl-json < 8
Obsoletes: php-pecl-jsonc < 8
Provides: php-json = %{upver}, php-json%{?_isa} = %{upver}
Provides: php-libxml, php-libxml%{?_isa}
Provides: php-openssl, php-openssl%{?_isa}
Provides: php-phar, php-phar%{?_isa}
Provides: php-pcre, php-pcre%{?_isa}
Provides: php-reflection, php-reflection%{?_isa}
Provides: php-session, php-session%{?_isa}
Provides: php-sockets, php-sockets%{?_isa}
Provides: php-spl, php-spl%{?_isa}
Provides: php-standard = %{version}, php-standard%{?_isa} = %{version}
Provides: php-tokenizer, php-tokenizer%{?_isa}
Provides: php-zlib, php-zlib%{?_isa}

Obsoletes: php-pecl-phar < 1.2.4
Obsoletes: php-pecl-Fileinfo < 1.0.5
Provides:  php-pecl-Fileinfo = %{fileinfover}, php-pecl-Fileinfo%{?_isa} = %{fileinfover}
Provides:  php-pecl(Fileinfo) = %{fileinfover}, php-pecl(Fileinfo)%{?_isa} = %{fileinfover}
Obsoletes: php-mhash < 5.3.0
%if 0%{?rhel} == 7
Obsoletes: php53-mhash, php53u-mhash
Obsoletes: php53-common, php53u-common, php54-common, php54w-common, php55u-common, php55w-common, php56u-common, php56w-common
Obsoletes: php70u-common, php70w-common, php71u-common, php71w-common, php72u-common, php72w-common
Obsoletes: php73-common, php73w-common
Obsoletes: php74-common, php74w-common
Obsoletes: php80-common
# Json
Obsoletes: php53-json, php53u-json, php54-json, php54w-json, php55u-json, php55w-json, php56u-json, php56w-json
Obsoletes: php55u-pecl-jsonc, php56u-pecl-jsonc
Obsoletes: php70u-json, php70w-json, php71u-json, php71w-json, php72u-json, php72w-json
Obsoletes: php73-json, php73w-json
Obsoletes: php74-json, php74w-json
# Xmlrpc
Obsoletes: php53-xmlrpc, php53u-xmlrpc, php54-xmlrpc, php54w-xmlrpc, php55u-xmlrpc, php55w-xmlrpc, php56u-xmlrpc, php56w-xmlrpc
Obsoletes: php70u-xmlrpc, php70w-xmlrpc, php71u-xmlrpc, php71w-xmlrpc, php72u-xmlrpc, php72w-xmlrpc
Obsoletes: php73-xmlrpc, php73w-xmlrpc
Obsoletes: php74-xmlrpc, php74w-xmlrpc
%endif

%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Summary: Files needed for building PHP extensions
Requires: php-cli%{?_isa} = %{version}-%{release}
# always needed to build extension
Requires: autoconf
Requires: automake
Requires: make
Requires: gcc
Requires: gcc-c++
Requires: libtool
# see "php-config --libs"
Requires: krb5-devel%{?_isa}
Requires: libxml2-devel%{?_isa}
Requires: openssl-devel%{?_isa} >= 1.0.1
%if %{with libpcre}
Requires: pcre2-devel%{?_isa}
%endif
Requires: zlib-devel%{?_isa}
Obsoletes: php-pecl-json-devel  < %{version}
Obsoletes: php-pecl-jsonc-devel < %{version}
%if %{with zts}
Provides: php-zts-devel = %{version}-%{release}
Provides: php-zts-devel%{?_isa} = %{version}-%{release}
%endif
%if 0%{?rhel} == 7
Obsoletes: php53-devel, php53u-devel, php54-devel, php54w-devel, php55u-devel, php55w-devel, php56u-devel, php56w-devel
Obsoletes: php55u-pecl-jsonc-devel, php56u-pecl-jsonc-devel
Obsoletes: php70u-devel, php70w-devel, php71u-devel, php71w-devel, php72u-devel, php72w-devel
Obsoletes: php73-devel, php73w-devel
Obsoletes: php74-devel, php74w-devel
Obsoletes: php80-devel
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Recommends: php-nikic-php-parser4 >= 4.13.0
%endif

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package opcache
Summary:   The Zend OPcache
License:   PHP
Requires:  php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-zendopcache < 7.0.6
Provides:  php-pecl-zendopcache = %{version}
Provides:  php-pecl-zendopcache%{?_isa} = %{version}
Provides:  php-pecl(opcache) = %{version}
Provides:  php-pecl(opcache)%{?_isa} = %{version}
%if 0%{?rhel} == 7
Obsoletes: php55u-opcache, php55w-opcache, php56u-opcache, php56w-opcache
Obsoletes: php70u-opcache, php70w-opcache, php71u-opcache, php71w-opcache, php72u-opcache, php72w-opcache
Obsoletes: php73-opcache, php73w-opcache
Obsoletes: php74-opcache, php74w-opcache
Obsoletes: php80-opcache
%endif

%description opcache
The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.

%if %{with imap}
%package imap
Summary: A module for PHP applications that use IMAP
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(krb5)
BuildRequires: pkgconfig(krb5-gssapi)
BuildRequires: openssl-devel >= 1.0.1
BuildRequires: libc-client-devel
%if 0%{?rhel} == 7
Obsoletes: php53-imap, php53u-imap, php54-imap, php54w-imap, php55u-imap, php55w-imap, php56u-imap, php56w-imap
Obsoletes: php70u-imap, php70w-imap, php71u-imap, php71w-imap, php72u-imap, php72w-imap
Obsoletes: php73-imap, php73w-imap
Obsoletes: php74-imap, php74w-imap
Obsoletes: php80-imap
%endif

%description imap
The php-imap module will add IMAP (Internet Message Access Protocol)
support to PHP. IMAP is a protocol for retrieving and uploading e-mail
messages on mail servers. PHP is an HTML-embedded scripting language.
%endif

%package ldap
Summary: A module for PHP applications that use LDAP
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(libsasl2)
BuildRequires: openldap-devel
BuildRequires: openssl-devel >= 1.0.1
%if 0%{?rhel} == 7
Obsoletes: php53-ldap, php53u-ldap, php54-ldap, php54w-ldap, php55u-ldap, php55w-ldap, php56u-ldap, php56w-ldap
Obsoletes: php70u-ldap, php70w-ldap, php71u-ldap, php71w-ldap, php72u-ldap, php72w-ldap
Obsoletes: php73-ldap, php73w-ldap
Obsoletes: php74-ldap, php74w-ldap
Obsoletes: php80-ldap
%endif

%description ldap
The php-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.

%package pdo
Summary: A database access abstraction module for PHP applications
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
# ABI/API check - Arch specific
Provides: php-pdo-abi  = %{pdover}-%{__isa_bits}
Provides: php(pdo-abi) = %{pdover}-%{__isa_bits}
Provides: php-sqlite3, php-sqlite3%{?_isa}
Provides: php-pdo_sqlite, php-pdo_sqlite%{?_isa}
%if 0%{?rhel} == 7
Obsoletes: php53-pdo, php53u-pdo, php54-pdo, php54w-pdo, php55u-pdo, php55w-pdo, php56u-pdo, php56w-pdo
Obsoletes: php70u-pdo, php70w-pdo, php71u-pdo, php71w-pdo, php72u-pdo, php72w-pdo
Obsoletes: php73-pdo, php73w-pdo
Obsoletes: php74-pdo, php74w-pdo
Obsoletes: php80-pdo
%endif

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.

%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-mysqli = %{version}-%{release}
Provides: php-mysqli%{?_isa} = %{version}-%{release}
Provides: php-pdo_mysql, php-pdo_mysql%{?_isa}
Obsoletes: php-mysql < %{version}-%{release}
%if 0%{?rhel} == 7
Obsoletes: php53-mysqlnd, php53u-mysqlnd, php54-mysqlnd, php54w-mysqlnd, php55u-mysqlnd, php55w-mysqlnd, php56u-mysqlnd, php56w-mysqlnd
Obsoletes: php70u-mysqlnd, php70w-mysqlnd, php71u-mysqlnd, php71w-mysqlnd, php72u-mysqlnd, php72w-mysqlnd
Obsoletes: php73-mysqlnd, php73w-mysqlnd
Obsoletes: php74-mysqlnd, php74w-mysqlnd
Obsoletes: php80-mysqlnd
Obsoletes: php53-mysql, php53u-mysql, php54-mysql, php54w-mysql, php55u-mysql, php55w-mysql, php56u-mysql, php56w-mysql
Obsoletes: php70u-mysql, php70w-mysql, php71u-mysql, php71w-mysql, php72u-mysql, php72w-mysql
%endif

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver

%package pgsql
Summary: A PostgreSQL database module for PHP
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_pgsql, php-pdo_pgsql%{?_isa}
BuildRequires: krb5-devel
BuildRequires: openssl-devel >= 1.0.1
BuildRequires: postgresql-devel
%if 0%{?rhel} == 7
Obsoletes: php53-pgsql, php53u-pgsql, php54-pgsql, php54w-pgsql, php55u-pgsql, php55w-pgsql, php56u-pgsql, php56w-pgsql
Obsoletes: php70u-pgsql, php70w-pgsql, php71u-pgsql, php71w-pgsql, php72u-pgsql, php72w-pgsql
Obsoletes: php73-pgsql, php73w-pgsql
Obsoletes: php74-pgsql, php74w-pgsql
Obsoletes: php80-pgsql
%endif

%description pgsql
The php-pgsql package add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package process
Summary: Modules for PHP script using system process interfaces
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-posix, php-posix%{?_isa}
Provides: php-shmop, php-shmop%{?_isa}
Provides: php-sysvsem, php-sysvsem%{?_isa}
Provides: php-sysvshm, php-sysvshm%{?_isa}
Provides: php-sysvmsg, php-sysvmsg%{?_isa}
%if 0%{?rhel} == 7
Obsoletes: php53-process, php53u-process, php54-process, php54w-process, php55u-process, php55w-process, php56u-process, php56w-process
Obsoletes: php70u-process, php70w-process, php71u-process, php71w-process, php72u-process, php72w-process
Obsoletes: php73-process, php73w-process
Obsoletes: php74-process, php74w-process
Obsoletes: php80-process
%endif

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Summary: A module for PHP applications that use ODBC databases
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_odbc, php-pdo_odbc%{?_isa}
# EL-7 version don't have pkgconfig
BuildRequires: unixODBC-devel
%if 0%{?rhel} == 7
Obsoletes: php53-odbc, php53u-odbc, php54-odbc, php54w-odbc, php55u-odbc, php55w-odbc, php56u-odbc, php56w-odbc
Obsoletes: php70u-odbc, php70w-odbc, php71u-odbc, php71w-odbc, php72u-odbc, php72w-odbc
Obsoletes: php73-odbc, php73w-odbc
Obsoletes: php74-odbc, php74w-odbc
Obsoletes: php80-odbc
%endif

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Summary: A module for PHP applications that use the SOAP protocol
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(libxml-2.0)
%if 0%{?rhel} == 7
Obsoletes: php53-soap, php53u-soap, php54-soap, php54w-soap, php55u-soap, php55w-soap, php56u-soap, php56w-soap
Obsoletes: php70u-soap, php70w-soap, php71u-soap, php71w-soap, php72u-soap, php72w-soap
Obsoletes: php73-soap, php73w-soap
Obsoletes: php74-soap, php74w-soap
Obsoletes: php80-soap
%endif

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%if %{with firebird}
%package pdo-firebird
Summary: PDO driver for Interbase/Firebird databases
# All files licensed under PHP version 3.01
License: PHP
BuildRequires:  firebird-devel
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_firebird, php-pdo_firebird%{?_isa}
%if 0%{?rhel} == 7
Obsoletes: php53-interbase, php53u-interbase, php54-interbase, php54w-interbase, php55u-interbase, php55w-interbase, php56u-interbase, php56w-interbase
Obsoletes: php70u-interbase, php70w-interbase, php71u-interbase, php71w-interbase, php72u-interbase, php72w-interbase
Obsoletes: php73-interbase, php73w-interbase
Obsoletes: php74-pdo-firebird, php74w-pdo-firebird
Obsoletes: php80-pdo-firebird
%endif

%description pdo-firebird
The php-pdo-firebird package contains the PDO driver for
Interbase/Firebird databases.
%endif

%if %{with oci8}
%package oci8
Summary:        A module for PHP applications that use OCI8 databases
# All files licensed under PHP version 3.01
License:        PHP
BuildRequires: (oracle-instantclient-devel >= %{oraclever} with oracle-instantclient-devel < %{oraclemax})
Requires:       php-pdo%{?_isa} = %{version}-%{release}
Provides:       php_database
Provides:       php-pdo_oci
Provides:       php-pdo_oci%{?_isa}
Obsoletes:      php-pecl-oci8         <= %{oci8ver}
Conflicts:      php-pecl-oci8         >  %{oci8ver}
Provides:       php-pecl(oci8)         = %{oci8ver}
Provides:       php-pecl(oci8)%{?_isa} = %{oci8ver}
%if 0%{?rhel} == 7
Obsoletes:      php53-oci8, php53u-oci8, php54-oci8, php54w-oci8, php55u-oci8, php55w-oci8, php56u-oci8, php56w-oci8
Obsoletes:      php70u-oci8, php70w-oci8, php71u-oci8, php71w-oci8, php72u-oci8, php72w-oci8
Obsoletes:      php73-oci8, php73w-oci8
Obsoletes:      php74-oci8, php74w-oci8
Obsoletes:      php80-oci8
%endif

%description oci8
The php-oci8 packages provides the OCI8 extension version %{oci8ver}
and the PDO driver to access Oracle Database.

The extension is linked with Oracle client libraries %{oraclever}
(Oracle Instant Client).  For details, see Oracle's note
"Oracle Client / Server Interoperability Support" (ID 207303.1).

You must install libclntsh.so.%{oraclelib} to use this package,
provided by Oracle Instant Client RPM available from Oracle on:
https://www.oracle.com/database/technologies/instant-client/downloads.html

Documentation is at http://php.net/oci8 and http://php.net/pdo_oci
%endif

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel
%if 0%{?rhel} == 7
Obsoletes: php53-snmp, php53u-snmp, php54-snmp, php54w-snmp, php55u-snmp, php55w-snmp, php56u-snmp, php56w-snmp
Obsoletes: php70u-snmp, php70w-snmp, php71u-snmp, php71w-snmp, php72u-snmp, php72w-snmp
Obsoletes: php73-snmp, php73w-snmp
Obsoletes: php74-snmp, php74w-snmp
Obsoletes: php80-snmp
%endif

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-dom, php-dom%{?_isa}
Provides: php-domxml, php-domxml%{?_isa}
Provides: php-simplexml, php-simplexml%{?_isa}
Provides: php-xmlreader, php-xmlreader%{?_isa}
Provides: php-xmlwriter, php-xmlwriter%{?_isa}
Provides: php-xsl, php-xsl%{?_isa}
BuildRequires: pkgconfig(libxslt)  >= 1.1
BuildRequires: pkgconfig(libexslt)
BuildRequires: pkgconfig(libxml-2.0)  >= 2.7.6
%if 0%{?rhel} == 7
Obsoletes: php53-xml, php53u-xml, php54-xml, php54w-xml, php55u-xml, php55w-xml, php56u-xml, php56w-xml
Obsoletes: php70u-xml, php70w-xml, php71u-xml, php71w-xml, php72u-xml, php72w-xml
Obsoletes: php73-xml, php73w-xml
Obsoletes: php74-xml, php74w-xml
Obsoletes: php80-xml
%endif

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
# All files licensed under PHP version 3.01, except
# libmbfl is licensed under LGPLv2
# onigurama is licensed under BSD
# ucgendat is licensed under OpenLDAP
License: PHP and LGPLv2 and BSD and OpenLDAP
%if 0%{?rhel}
BuildRequires: oniguruma5php-devel
%else
BuildRequires: oniguruma-devel
%endif
Provides: bundled(libmbfl) = 1.3.2
Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel} == 7
Obsoletes: php53-mbstring, php53u-mbstring, php54-mbstring, php54w-mbstring, php55u-mbstring, php55w-mbstring, php56u-mbstring, php56w-mbstring
Obsoletes: php70u-mbstring, php70w-mbstring, php71u-mbstring, php71w-mbstring, php72u-mbstring, php72w-mbstring
Obsoletes: php73-mbstring, php73w-mbstring
Obsoletes: php74-mbstring, php74w-mbstring
Obsoletes: php80-mbstring
%endif

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
# All files licensed under PHP version 3.01
%if %{with libgd}
License: PHP
%else
# bundled libgd is licensed under BSD
License: PHP and BSD
%endif
Requires: php-common%{?_isa} = %{version}-%{release}
%if %{with libgd}
%if 0%{?rhel}
BuildRequires: gd3php-devel >= 2.3.3
%else
BuildRequires: pkgconfig(gdlib) >= 2.3.3
%endif
%else
# Required to build the bundled GD library
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(xpm)
BuildRequires: pkgconfig(libwebp)
Provides: bundled(gd) = 2.0.35
%endif
%if 0%{?rhel} == 7
Obsoletes: php53-gd, php53u-gd, php54-gd, php54w-gd, php55u-gd, php55w-gd, php56u-gd, php56w-gd
Obsoletes: php70u-gd, php70w-gd, php71u-gd, php71w-gd, php72u-gd, php72w-gd
Obsoletes: php73-gd, php73w-gd
Obsoletes: php74-gd, php74w-gd
Obsoletes: php80-gd
%endif

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel} == 7
Obsoletes: php53-bcmath, php53u-bcmath, php54-bcmath, php54w-bcmath, php55u-bcmath, php55w-bcmath, php56u-bcmath, php56w-bcmath
Obsoletes: php70u-bcmath, php70w-bcmath, php71u-bcmath, php71w-bcmath, php72u-bcmath, php72w-bcmath
Obsoletes: php73-bcmath, php73w-bcmath
Obsoletes: php74-bcmath, php74w-bcmath
Obsoletes: php80-bcmath
%endif
Provides: bundled(libbcmath)

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package gmp
Summary: A module for PHP applications for using the GNU MP library
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: gmp-devel
Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel} == 7
Obsoletes: php53-gmp, php53u-gmp, php54-gmp, php54w-gmp, php55u-gmp, php55w-gmp, php56u-gmp, php56w-gmp
Obsoletes: php70u-gmp, php70w-gmp, php71u-gmp, php71w-gmp, php72u-gmp, php72w-gmp
Obsoletes: php73-gmp, php73w-gmp
Obsoletes: php74-gmp, php74w-gmp
Obsoletes: php80-gmp
%endif

%description gmp
These functions allow you to work with arbitrary-length integers
using the GNU MP library.

%package dba
Summary: A database abstraction layer module for PHP applications
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: libdb-devel
BuildRequires: tokyocabinet-devel
BuildRequires: lmdb-devel
%if %{with qdbm}
BuildRequires: qdbm-devel
%endif
Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel} == 7
Obsoletes: php53-dba, php53u-dba, php54-dba, php54w-dba, php55u-dba, php55w-dba, php56u-dba, php56w-dba
Obsoletes: php70u-dba, php70w-dba, php71u-dba, php71w-dba, php72u-dba, php72w-dba
Obsoletes: php73-dba, php73w-dba
Obsoletes: php74-dba, php74w-dba
Obsoletes: php80-dba
%endif

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%package tidy
Summary: Standard PHP module provides tidy library support
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libtidy-devel
%if 0%{?rhel} == 7
Obsoletes: php53-tidy, php53u-tidy, php54-tidy, php54w-tidy, php55u-tidy, php55w-tidy, php56u-tidy, php56w-tidy
Obsoletes: php70u-tidy, php70w-tidy, php71u-tidy, php71w-tidy, php72u-tidy, php72w-tidy
Obsoletes: php73-tidy, php73w-tidy
Obsoletes: php74-tidy, php74w-tidy
Obsoletes: php80-tidy
%endif

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.

%package pdo-dblib
Summary: PDO driver for Microsoft SQL Server and Sybase databases
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
BuildRequires: freetds-devel >= 0.91
Provides: php-pdo_dblib, php-pdo_dblib%{?_isa}
Obsoletes: php-mssql < %{version}-%{release}
%if 0%{?rhel} == 7
Obsoletes: php53-mssql, php53u-mssql, php54-mssql, php54w-mssql, php55u-mssql, php55w-mssql, php56u-mssql, php56w-mssql
Obsoletes: php70u-pdo-dblib, php70w-pdo_dblib, php71u-pdo-dblib, php71w-pdo_dblib, php72u-pdo-dblib, php72w-pdo_dblib
Obsoletes: php73-pdo-dblib, php73w-pdo_dblib
Obsoletes: php74-pdo-dblib, php74w-pdo_dblib
Obsoletes: php80-pdo-dblib
%endif

%description pdo-dblib
The php-pdo-dblib package contains a dynamic shared object
that implements the PHP Data Objects (PDO) interface to enable access from
PHP to Microsoft SQL Server and Sybase databases through the FreeTDS library.

%package embedded
Summary: PHP library for embedding in applications
Requires: php-common%{?_isa} = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: php-embedded-devel = %{version}-%{release}
Provides: php-embedded-devel%{?_isa} = %{version}-%{release}
%if 0%{?rhel} == 7
Obsoletes: php53-embedded, php53u-embedded, php54-embedded, php54w-embedded, php55u-embedded, php55w-embedded, php56u-embedded, php56w-embedded
Obsoletes: php70u-embedded, php70w-embedded, php71u-embedded, php71w-embedded, php72u-embedded, php72w-embedded
Obsoletes: php73-embedded, php73w-embedded
Obsoletes: php74-embedded, php74w-embedded
Obsoletes: php80-embedded
%endif

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

%package pspell
Summary: A module for PHP applications for using pspell interfaces
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0
%if 0%{?rhel} == 7
Obsoletes: php53-pspell, php53u-pspell, php54-pspell, php54w-pspell, php55u-pspell, php55w-pspell, php56u-pspell, php56w-pspell
Obsoletes: php70u-pspell, php70w-pspell, php71u-pspell, php71w-pspell, php72u-pspell, php72w-pspell
Obsoletes: php73-pspell, php73w-pspell
Obsoletes: php74-pspell, php74w-pspell
Obsoletes: php80-pspell
%endif

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%package intl
Summary: Internationalization extension for PHP applications
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(icu-i18n) >= 78
BuildRequires: pkgconfig(icu-io)   >= 78
BuildRequires: pkgconfig(icu-uc)   >= 78
%if 0%{?rhel} == 7
Obsoletes: php53-intl, php53u-intl, php54-intl, php54w-intl, php55u-intl, php55w-intl, php56u-intl, php56w-intl
Obsoletes: php70u-intl, php70w-intl, php71u-intl, php71w-intl, php72u-intl, php72w-intl
Obsoletes: php73-intl, php73w-intl
Obsoletes: php74-intl, php74w-intl
Obsoletes: php80-intl
%endif

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%package enchant
Summary: Enchant spelling extension for PHP applications
# All files licensed under PHP version 3.0
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(enchant-2)
%if 0%{?rhel} == 7
Obsoletes: php53-enchant, php53u-enchant, php54-enchant, php54w-enchant, php55u-enchant, php55w-enchant, php56u-enchant, php56w-enchant
Obsoletes: php70u-enchant, php70w-enchant, php71u-enchant, php71w-enchant, php72u-enchant, php72w-enchant
Obsoletes: php73-enchant, php73w-enchant
Obsoletes: php74-enchant, php74w-enchant
Obsoletes: php80-enchant
%endif

%description enchant
The php-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.

%if %{with zip}
%package zip
Summary: ZIP archive management extension for PHP
# All files licensed under PHP version 3.0.1
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-zip          < %{zipver}
Provides:  php-pecl(zip)         = %{zipver}
Provides:  php-pecl(zip)%{?_isa} = %{zipver}
Provides:  php-pecl-zip          = %{zipver}
Provides:  php-pecl-zip%{?_isa}  = %{zipver}
%if 0%{?rhel} == 7
Obsoletes: php53-zip, php53u-zip, php54-zip, php54w-zip, php55u-zip, php55w-zip, php56u-zip, php56w-zip
Obsoletes: php70u-zip, php70w-zip, php71u-zip, php71w-zip, php72u-zip, php72w-zip
Obsoletes: php73-zip, php73w-zip
Obsoletes: php74-zip, php74w-zip
Obsoletes: php80-zip
%endif
BuildRequires: pkgconfig(libzip) >= 0.11

%description zip
The php-zip package provides an extension that will add
support for ZIP archive management to PHP.
%endif

%package sodium
Summary: Wrapper for the Sodium cryptographic library
# All files licensed under PHP version 3.0.1
License: PHP
# Minimal is 1.0.8, 1.0.14 is needed for argon2 password
BuildRequires:  pkgconfig(libsodium) >= 1.0.14

Requires: php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-libsodium2 < 3
Provides:  php-pecl(libsodium)         = %{version}
Provides:  php-pecl(libsodium)%{?_isa} = %{version}
%if 0%{?rhel} == 7
Obsoletes: php72u-sodium, php72w-sodium
Obsoletes: php73-sodium, php73w-sodium
Obsoletes: php74-sodium, php74w-sodium
Obsoletes: php80-sodium
%endif

%description sodium
The php-sodium package provides a simple,
low-level PHP extension for the libsodium cryptographic library.


%package ffi
Summary: Foreign Function Interface
# All files licensed under PHP version 3.0.1
License: PHP
BuildRequires:  pkgconfig(libffi)

Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel} == 7
Obsoletes: php74-ffi, php74w-ffi
Obsoletes: php80-ffi
%endif

%description ffi
FFI is one of the features that made Python and LuaJIT very useful for fast
prototyping. It allows calling C functions and using C data types from pure
scripting language and therefore develop “system code” more productively.

For PHP, FFI opens a way to write PHP extensions and bindings to C libraries
in pure PHP.


%prep
: Building %{name}-%{version}-%{release}
%if %{with lsws}
: With Litespeed SAPI
%endif
%if %{with oci8}
: With Oracle extensions
%endif
%if %{with firebird}
: With pdo_firebird extension
%endif
%if %{with zip}
: With Zip extension
%endif
%if %{with tests}
: Run Test suite
%endif
%if %{with libgd}
: Use System libgd
%else
: Use Bundled libgd
%endif
%if %{with libpcre}
: Use System libpcre
%else
: Use Bundled libpcre
%endif
%if %{with zts}
: Enable ZTS build
%endif
%if %{with debug}
: Enable Debug build
%endif
%if %{with dtrace}
: Enable Dtrace build
%endif

%{?gpgverify:%{gpgverify} --keyring='%{SOURCE20}' --signature='%{SOURCE21}' --data='%{SOURCE0}'}

%setup -q -n php-%{upver}%{?rcver}

%patch -P1 -p1 -b .mpmcheck
%patch -P5 -p1 -b .includedir
%patch -P6 -p1 -b .embed
%patch -P7 -p1 -b .libdb
%patch -P9 -p1 -b .deprecated
%patch -P11 -p1 -b .icu74
%patch -P12 -p1 -b .proto
%patch -P13 -p1 -b .bash53

%patch -P41 -p1 -b .syslib
%patch -P42 -p1 -b .systzdata
%patch -P43 -p1 -b .headers
%patch -P45 -p1 -b .ldap_r
%patch -P46 -p1 -b .argon2
%patch -P47 -p1 -b .phpinfo
%patch -P48 -p1 -b .sha
%patch -P49 -p1 -b .pharsha
%if 0%{?fedora} >= 36 || 0%{?rhel} >= 9
%patch -P50 -p1 -b .openssl3
rm ext/openssl/tests/p12_with_extra_certs.p12
%endif
%patch -P51 -p1 -b .libxcrypt
%patch -P52 -p1 -b .intlinfo

%patch -P91 -p1 -b .remi-oci8

# upstream patches

# security patches
%patch -P200 -p1 -b .cve2756
%patch -P201 -p1 -b .cve3096
%patch -P202 -p1 -b .cve5458
%patch -P203 -p1 -b .cve8925
%patch -P204 -p1 -b .cve8926
%patch -P205 -p1 -b .cve8927
%patch -P206 -p1 -b .cve9026
%patch -P207 -p1 -b .cve11236
%patch -P208 -p1 -b .cve11234
%patch -P209 -p1 -b .cve8932
%patch -P210 -p1 -b .cve11233
%patch -P211 -p1 -b .ghsa4w77
%patch -P212 -p1 -b .cve8929
%patch -P213 -p1 -b .cve1217
%patch -P214 -p1 -b .cve1734
%patch -P215 -p1 -b .cve1861
%patch -P216 -p1 -b .cve1736
%patch -P217 -p1 -b .cve1219
%patch -P218 -p1 -b .cve6491
%patch -P219 -p1 -b .cve1220
%patch -P220 -p1 -b .cve1735
%patch -P221 -p1 -b .cve14177
%patch -P222 -p1 -b .cve14178
%patch -P223 -p1 -b .ghsawwww2
%patch -P224 -p1 -b .cve14179
%patch -P225 -p1 -b .cve6722
%patch -P226 -p1 -b .cve7261
%patch -P227 -p1 -b .cve7262
%patch -P228 -p1 -b .cve6735
%patch -P229 -p1 -b .cve7259
%patch -P230 -p1 -b .cve7268
%patch -P231 -p1 -b .cve7258
%patch -P232 -p1 -b .gh22187
%patch -P233 -p1 -b .cve9672
%patch -P234 -p1 -b .cve17543
%patch -P235 -p1 -b .cve7260
%patch -P236 -p1 -b .gh22643
%patch -P237 -p1 -b .8234
%patch -P238 -p1 -b .cve109618

# Fixes for tests related to tzdata
%patch -P300 -p1 -b .datetests
%patch -P301 -p1 -b .zlibng
%patch -P302 -p1 -b .pcretests

# WIP patch

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/bcmath/libbcmath/LICENSE libbcmath_LICENSE
cp ext/date/lib/LICENSE.rst timelib_LICENSE

# Multiple builds for multiple SAPIs
mkdir build-cgi build-apache build-embedded \
%if %{with zts}
    build-ztscli \
%endif
    build-fpm

# ----- Manage known as failed test -------
# affected by systzdata patch
rm ext/date/tests/timezone_location_get.phpt
%if 0%{?fedora} < 36
# need tzdata 2022b
rm ext/date/tests/bug33414-1.phpt
rm ext/date/tests/bug33415-2.phpt
rm ext/date/tests/date_modify-1.phpt
%endif
# too fast builder
rm ext/date/tests/bug73837.phpt
# Should be skipped but fails sometime
rm ext/standard/tests/file/file_get_contents_error001.phpt
# fails sometime
rm ext/sockets/tests/mcast_ipv?_recv.phpt
# cause stack exhausion
rm Zend/tests/bug54268.phpt
rm Zend/tests/bug68412.phpt
# slow and erratic result
rm sapi/cli/tests/upload_2G.phpt
# tar issue
rm ext/zlib/tests/004-mb.phpt
# failed when systemd is enabled
rm sapi/fpm/tests/gh8885-stderr-fd-reload-usr1.phpt
rm sapi/fpm/tests/gh8885-stderr-fd-reload-usr2.phpt
# Known to fail
%if 0%{?rhel} == 8
rm ext/openssl/tests/openssl_error_string_basic.phpt
rm ext/openssl/tests/openssl_open_basic.phpt
%else
rm ext/openssl/tests/openssl_error_string_basic_openssl3.phpt
%endif
rm ext/openssl/tests/openssl_private_decrypt_basic.phpt
rm ext/openssl/tests/openssl_x509_parse_basic.phpt
rm ext/openssl/tests/sni_server.phpt
rm ext/openssl/tests/sni_server_key_cert.phpt
rm ext/openssl/tests/bug74341.phpt
rm ext/pcre/tests/pcre_extra.phpt
rm ext/pcre/tests/split.phpt
rm ext/pcre/tests/grep2.phpt

# avoid issue when 2 builds run simultaneously (keep 64321 for the SCL)
%ifarch x86_64
sed -e 's/64321/64322/' -i ext/openssl/tests/*.phpt
%else
sed -e 's/64321/64323/' -i ext/openssl/tests/*.phpt
%endif

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{upver}%{?rcver}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{upver}%{?rcver}.
   : Update the version/rcver macros and rebuild.
   exit 1
fi

vapi=$(sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h)
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=$(sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h)
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=$(sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h)
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_OCI8_VERSION /{s/.* "//;s/".*$//;p}' ext/oci8/php_oci8.h)
if test "$ver" != "%{oci8ver}"; then
   : Error: Upstream OCI8 version is now ${ver}, expecting %{oci8ver}.
   : Update the oci8ver macro and rebuild.
   exit 1
fi

ver=$(sed -n '/#define PHP_ZIP_VERSION /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
   : Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
   : Update the %{zipver} macro and rebuild.
   exit 1
fi

# https://bugs.php.net/63362 - Not needed but installed headers.
# Drop some Windows specific headers to avoid installation,
# before build to ensure they are really not needed.
rm -f TSRM/tsrm_win32.h \
      TSRM/tsrm_config.w32.h \
      Zend/zend_config.w32.h \
      ext/mysqlnd/config-win.h \
      ext/standard/winver.h \
      main/win32_internal_function_disabled.h \
      main/win95nt.h

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

# Some extensions have their own configuration file
cp %{SOURCE50} %{SOURCE51} %{SOURCE52} %{SOURCE53} .

# Regenerated bison files
# to force, rm Zend/zend_{language,ini}_parser.[ch]
if [ ! -f Zend/zend_language_parser.c ]; then
  scripts/dev/genfiles
fi


%build
# This package fails to build with LTO due to undefined symbols.  LTO
# was disabled in OpenSuSE as well, but with no real explanation why
# beyond the undefined symbols.  It really shold be investigated further.
# Disable LTO
%define _lto_cflags %{nil}

%{?dtsenable}

# Set build date from https://reproducible-builds.org/specs/source-date-epoch/
export SOURCE_DATE_EPOCH=$(date +%s -r NEWS)
export PHP_UNAME=$(uname)
export PHP_BUILD_SYSTEM=$(cat /etc/redhat-release | sed -e 's/ Beta//')
%if 0%{?vendor:1}
export PHP_BUILD_PROVIDER="%{vendor}"
%endif
export PHP_BUILD_COMPILER="$(gcc --version | head -n1)"
export PHP_BUILD_ARCH="%{_arch}"

# Force use of system libtool:
libtoolize --force --copy
cat $(aclocal --print-ac-dir)/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4

# Regenerate configure scripts (patches change config.m4's)
touch configure.ac
./buildconf --force
%if %{with debug}
LDFLAGS="-fsanitize=address"
export LDFLAGS
CFLAGS=$(echo $RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign  -fsanitize=address -ggdb | sed 's/-mstackrealign//')
%else
CFLAGS=$(echo $RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign | sed 's/-mstackrealign//')
%endif
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# Old/recent bison version seems to produce a broken parser;
# upstream uses GNU Bison 2.3. Workaround:
# Only provided in official tarball (not in snapshot)
if [ -f ../Zend/zend_language_parser.c ]; then
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
fi

# Always static:
# date, filter, libxml, reflection, spl: not supported
# hash: for PHAR_SIG_SHA256 and PHAR_SIG_SHA512
# session: dep on hash, used by soap
# pcre: used by filter, zip
# pcntl, readline: only used by CLI sapi
# openssl: for PHAR_SIG_OPENSSL
# zlib: used by image

ln -sf ../configure
%configure \
    --enable-rtld-now \
    --cache-file=../config.cache \
    --with-libdir=%{_lib} \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --disable-debug \
    --with-pic \
    --disable-rpath \
    --without-pear \
    --with-exec-dir=%{_bindir} \
    --without-gdbm \
    --with-openssl \
    --with-system-ciphers \
%if %{with libpcre}
    --with-external-pcre \
%endif
%if %{with libxcrypt}
    --with-external-libcrypt \
%endif
    --with-zlib \
    --with-layout=GNU \
    --with-kerberos \
    --with-libxml \
%if 0%{?fedora} >= 29 || 0%{?rhel} >= 6
    --with-system-tzdata \
%endif
    --with-mhash \
    --without-password-argon2 \
%if %{with dtrace}
    --enable-dtrace \
%endif
%if %{with debug}
    --enable-debug \
%endif
    $*
if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and most shared extensions
pushd build-cgi

build --libdir=%{_libdir}/php \
      --enable-pcntl \
      --enable-opcache \
      --enable-opcache-file \
      --enable-phpdbg \
%if %{with imap}
      --with-imap=shared --with-imap-ssl \
%endif
      --enable-mbstring=shared \
      --enable-mbregex \
      --enable-gd=shared \
%if %{with libgd}
      --with-external-gd \
%else
      --with-webp \
      --with-jpeg \
      --with-xpm \
      --with-freetype \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-tcadb=%{_prefix} \
                          --with-lmdb=%{_prefix} \
%if %{with qdbm}
                          --with-qdbm=%{_root_prefix} \
%endif
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
%if %{with oci8}
         --with-oci8=shared,instantclient,%{_prefix}/lib/oracle/%{oracledir}/client64/lib,%{oraclever} \
      --with-pdo-oci=shared,instantclient,%{_prefix}/lib/oracle/%{oracledir}/client64/lib,%{oraclever} \
%endif
%if %{with firebird}
      --with-pdo-firebird=shared \
%endif
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared \
      --with-pdo-dblib=shared,%{_prefix} \
      --with-sqlite3=shared \
%if %{with zip}
      --with-zip=shared \
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-tidy=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --with-ffi=shared \
      --with-sodium=shared \
      --enable-intl=shared \
      --with-enchant=shared
popd

without_shared="--disable-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-opcache \
      --disable-phpdbg \
      --without-ffi \
      --disable-xmlreader --disable-xmlwriter \
      --without-sodium \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --without-pspell \
      --without-curl --disable-posix --disable-xml \
      --disable-simplexml --disable-exif --without-gettext \
      --without-iconv --disable-ftp --without-bz2 --disable-ctype \
      --disable-shmop --disable-sockets --disable-tokenizer \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_httpd_apxs} \
      --libdir=%{_libdir}/php \
%if %{with lsws}
      --enable-litespeed \
%endif
      --without-mysqli \
      --disable-pdo \
      ${without_shared}
popd

# Build php-fpm
pushd build-fpm
build --enable-fpm \
      --with-fpm-systemd \
      --with-fpm-acl \
      --libdir=%{_libdir}/php \
      --without-mysqli \
      --disable-pdo \
      ${without_shared}
popd

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp.so
pushd build-embedded
build --enable-embed \
      --without-mysqli --disable-pdo \
      ${without_shared}
popd

%if %{with zts}
# Build a special thread-safe (mainly for modules)
pushd build-ztscli

EXTENSION_DIR=%{_libdir}/php-zts/modules
build --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-zts \
      --program-prefix=zts- \
      --disable-cgi \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --enable-pcntl \
      --enable-opcache \
      --enable-opcache-file \
%if %{with imap}
      --with-imap=shared --with-imap-ssl \
%endif
      --enable-mbstring=shared \
      --enable-mbregex \
      --enable-gd=shared \
%if %{with libgd}
      --with-external-gd \
%else
      --with-webp \
      --with-jpeg \
      --with-xpm \
      --with-freetype \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-tcadb=%{_prefix} \
                          --with-lmdb=%{_prefix} \
%if %{with qdbm}
                          --with-qdbm=%{_root_prefix} \
%endif
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --enable-mysqlnd-threading \
%if %{with oci8}
         --with-oci8=shared,instantclient,%{_prefix}/lib/oracle/%{oracledir}/client64/lib,%{oraclever} \
      --with-pdo-oci=shared,instantclient,%{_prefix}/lib/oracle/%{oracledir}/client64/lib,%{oraclever} \
%endif
%if %{with firebird}
      --with-pdo-firebird=shared \
%endif
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared \
      --with-pdo-dblib=shared,%{_prefix} \
      --with-sqlite3=shared \
%if %{with zip}
      --with-zip=shared \
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-tidy=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --with-ffi=shared \
      --with-sodium=shared \
      --enable-intl=shared \
      --with-enchant=shared
popd

### NOTE!!! EXTENSION_DIR was changed for the -zts build, so it must remain
### the last SAPI to be built.
%endif


%check
: Ensure proper NTS/ZTS build
$RPM_BUILD_ROOT%{_bindir}/php     -n -v | grep NTS
%if %{with zts}
$RPM_BUILD_ROOT%{_bindir}/zts-php -n -v | grep ZTS
%endif

%if %{with tests}
cd build-fpm

# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
export SKIP_ONLINE_TESTS=1
export SKIP_IO_CAPTURE_TESTS=1
unset TZ LANG LC_ALL
if ! make test TESTS=-j4; then
  set +x
  for f in $(find .. -name \*.diff -type f -print); do
    if ! grep -q XFAIL "${f/.diff/.phpt}"
    then
      echo "TEST FAILURE: $f --"
      head -n 100 "$f"
      echo -e "\n-- $f result ends."
    fi
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif


%install
%{?dtsenable}

%if %{with zts}
# Install the extensions for the ZTS version
make -C build-ztscli install \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the php-fpm binary
make -C build-fpm install-fpm \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install everything from the CGI SAPI build
make -C build-cgi install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Use php-config from embed SAPI to reduce used libs
install -m 755 build-embedded/scripts/php-config $RPM_BUILD_ROOT%{_bindir}/php-config

# Install the default configuration file
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/php/preload

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp.so

# Apache config fragment
# Dual config file with httpd >= 2.4 (fedora >= 18)
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_modconfdir}/20-php.conf
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf

%if %{with_httpd2410}
cat %{SOURCE11} >>$RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%else
mkdir _fpmdoc
cat %{SOURCE1} %{SOURCE11} >_fpmdoc/httpd-php.conf
cat << 'EOF' >_fpmdoc/README
To use FPM with Apache HTTP server:
- copy the httpd-php.conf to %{_httpd_confdir}/php.conf

To use FPM with NGINX web server:
- copy the nginx-fpm.conf to %{_sysconfdir}/nginx/conf.d/php-fpm.conf
- copy the nginx-php.conf to %{_sysconfdir}/nginx/default.d/php.conf
EOF
%endif

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%if %{with zts}
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d
%endif
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/wsdlcache
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/opcache
%if 0%{?fedora} >= 24 || 0%{?rhel} >= 8
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/peclxml
install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/pecl
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/tests/pecl
%endif

%if %{with lsws}
install -m 755 build-apache/sapi/litespeed/php $RPM_BUILD_ROOT%{_bindir}/lsphp
%endif

# PHP-FPM stuff
# Log
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
# Config
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf.default .
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf.default .
# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php-fpm

# Environment file
%if 0%{?fedora} < 26 && 0%{?rhel} < 8
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/php-fpm
%endif

install -m 755 -d $RPM_BUILD_ROOT/run/php-fpm
# install systemd unit files and scripts for handling server startup
# this folder requires systemd >= 204
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/php-fpm.service.d
install -Dm 644 %{SOURCE6}  $RPM_BUILD_ROOT%{_unitdir}/php-fpm.service
%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
install -Dm 644 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/httpd.service.d/php-fpm.conf
install -Dm 644 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/nginx.service.d/php-fpm.conf
%endif

%if 0%{?fedora} >= 26 || 0%{?rhel} >= 8
sed -e '/EnvironmentFile/d' -i $RPM_BUILD_ROOT%{_unitdir}/php-fpm.service
%endif

%if %{with_nginx}
# Nginx configuration
install -D -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/php-fpm.conf
install -D -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/php.conf

# Switch to UDS
# FPM
sed -e 's@127.0.0.1:9000@/run/php-fpm/www.sock@' \
    -e 's@^;listen.acl_users@listen.acl_users@' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
# Nginx
sed -e 's@127.0.0.1:9000@unix:/run/php-fpm/www.sock@' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/php-fpm.conf
# Apache
sed -e 's@proxy:fcgi://127.0.0.1:9000@proxy:unix:/run/php-fpm/www.sock|fcgi://localhost@' \
    -i $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%else
install -D -m 644 %{SOURCE13} _fpmdoc/nginx-fpm.conf
install -D -m 644 %{SOURCE14} _fpmdoc/nginx-php.conf
%endif

TESTCMD="$RPM_BUILD_ROOT%{_bindir}/php --no-php-ini"
# Ensure all provided extensions are really there
for mod in core date filter hash json libxml openssl pcntl pcre readline reflection session spl standard zlib
do
     $TESTCMD --modules | grep -i "$mod\$"
done

TESTCMD="$TESTCMD --define extension_dir=$RPM_BUILD_ROOT%{_libdir}/php/modules"

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql odbc ldap snmp \
%if %{with imap}
    imap \
%endif
    mysqlnd mysqli \
    mbstring gd dom xsl soap bcmath dba \
    simplexml bz2 calendar ctype exif ftp gettext gmp iconv \
    sockets tokenizer opcache \
    pdo \
%if %{with zip}
    zip \
%endif
    sqlite3 \
    enchant phar fileinfo intl \
    ffi \
    tidy pspell curl \
    sodium \
    posix shmop sysvshm sysvsem sysvmsg xml \
    pdo_mysql pdo_pgsql pdo_odbc pdo_sqlite pdo_dblib \
%if %{with oci8}
    oci8 pdo_oci \
%endif
%if %{with firebird}
    pdo_firebird \
%endif
    xmlreader xmlwriter
do
    case $mod in
      opcache)
        # Zend extensions
        TESTCMD="$TESTCMD --define zend_extension=$mod"
        ini=10-${mod}.ini;;
      pdo_*|mysqli|xmlreader)
        # Extensions with dependencies on 20-*
        TESTCMD="$TESTCMD --define extension=$mod"
        ini=30-${mod}.ini;;
      *)
        # Extensions with no dependency
        TESTCMD="$TESTCMD --define extension=$mod"
        ini=20-${mod}.ini;;
    esac

    $TESTCMD --modules | grep -i "$mod\$"

    # some extensions have their own config file
    if [ -f ${ini} ]; then
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini}
      %if %{with zts}
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini}
      %endif
    else
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}
EOF
%if %{with zts}
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}
EOF
%endif
    fi
    cat > files.${mod} <<EOF
%{_libdir}/php/modules/${mod}.so
%config(noreplace) %{_sysconfdir}/php.d/${ini}
%if %{with zts}
%{_libdir}/php-zts/modules/${mod}.so
%config(noreplace) %{_sysconfdir}/php-zts.d/${ini}
%endif
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} \
    files.simplexml >> files.xml

# mysqlnd
cat files.mysqli \
    files.pdo_mysql \
    >> files.mysqlnd

# Split out the PDO modules
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc
%if %{with oci8}
cat files.pdo_oci >> files.oci8
%endif

# sysv* and posix in packaged in php-process
cat files.shmop files.sysv* files.posix > files.process

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
cat files.sqlite3 >> files.pdo

# Package curl, phar and fileinfo in -common.
cat files.curl files.phar files.fileinfo \
    files.exif files.gettext files.iconv files.calendar \
    files.ftp files.bz2 files.ctype files.sockets \
    files.tokenizer > files.common

# The default Zend OPcache blacklist file
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache-default.blacklist
%if %{with zts}
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/opcache-default.blacklist
sed -e '/blacklist_filename/s/php.d/php-zts.d/' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/10-opcache.ini
%endif

# Install the macros file:
sed -e "s/@PHP_APIVER@/%{apiver}-%{__isa_bits}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}-%{__isa_bits}/" \
    -e "s/@PHP_PDOVER@/%{pdover}-%{__isa_bits}/" \
    -e "s/@PHP_VERSION@/%{upver}/" \
%if %{without zts}
    -e "/zts/d" \
%endif
    < %{SOURCE3} > macros.php
%if 0%{?fedora} >= 24 || 0%{?rhel} >= 8
echo '%%pecl_xmldir   %%{_localstatedir}/lib/php/peclxml' >>macros.php
%endif
install -m 644 -D macros.php \
           $RPM_BUILD_ROOT%{macrosdir}/macros.php

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_bindir}/zts-phar* \
       $RPM_BUILD_ROOT%{_mandir}/man1/zts-phar* \
       $RPM_BUILD_ROOT%{_libdir}/libphp.a \
       $RPM_BUILD_ROOT%{_libdir}/libphp.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}


%pre common
%if %{?fedora}%{!?fedora:99} < 29
echo -e "WARNING : Fedora %{fedora} is now EOL :"
echo -e "You should consider upgrading to a supported release.\n"
%endif


%if ! %{with_httpd2410}
%pre fpm
# Add the "apache" user as we don't require httpd
getent group  apache >/dev/null || \
  groupadd -g 48 -r apache
getent passwd apache >/dev/null || \
  useradd -r -u 48 -g apache -s /sbin/nologin \
    -d %{_httpd_contentdir} -c "Apache" apache
exit 0
%endif

%post fpm
%systemd_post php-fpm.service

%preun fpm
%systemd_preun php-fpm.service

%if 0%{?fedora} < 27 && 0%{?rhel} < 8
%postun fpm
%systemd_postun_with_restart php-fpm.service
%endif

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
# Raised by new pool installation or new extension installation
%transfiletriggerin fpm -- %{_sysconfdir}/php-fpm.d %{_sysconfdir}/php.d
systemctl try-restart php-fpm.service >/dev/null 2>&1 || :
%endif

# Handle upgrading from SysV initscript to native systemd unit.
# We can tell if a SysV version of php-fpm was previously installed by
# checking to see if the initscript is present.
%triggerun fpm -- php-fpm
%if 0%{?fedora} >= 15
if [ -f /etc/rc.d/init.d/php-fpm ]; then
    # Save the current service runlevel info
    # User must manually run systemd-sysv-convert --apply php-fpm
    # to migrate them to systemd targets
    /usr/bin/systemd-sysv-convert --save php-fpm >/dev/null 2>&1 || :

    # Run these because the SysV package being removed won't do them
    /sbin/chkconfig --del php-fpm >/dev/null 2>&1 || :
    /bin/systemctl try-restart php-fpm.service >/dev/null 2>&1 || :
fi
%endif


%if 0%{?fedora} < 28 && 0%{?rhel} < 8
%post   embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig
%endif


%posttrans common
cat << EOF
=====================================================================

  WARNING : PHP 8.0 have reached its "End of Life" in
  November 2023. Even, if this package includes some of
  the important security fixes, backported from 8.2, the
  UPGRADE to a maintained version is very strongly RECOMMENDED.

=====================================================================
EOF


%{!?_licensedir:%global license %%doc}

%files
%{_httpd_moddir}/libphp.so
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/wsdlcache
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/opcache
%config(noreplace) %{_httpd_confdir}/php.conf
%config(noreplace) %{_httpd_modconfdir}/20-php.conf

%files common -f files.common
%doc EXTENSIONS NEWS UPGRADING* README.REDIST.BINS *md docs
%license LICENSE TSRM_LICENSE ZEND_LICENSE
%license libmagic_LICENSE
%license timelib_LICENSE
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%if %{with zts}
%dir %{_sysconfdir}/php-zts.d
%dir %{_libdir}/php-zts
%dir %{_libdir}/php-zts/modules
%endif
%dir %{_localstatedir}/lib/php
%if 0%{?fedora} >= 24 || 0%{?rhel} >= 8
%dir %{_localstatedir}/lib/php/peclxml
%dir %{_docdir}/pecl
%dir %{_datadir}/tests
%dir %{_datadir}/tests/pecl
%endif
%dir %{_datadir}/php

%files cli
%{_bindir}/php
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
# provides phpize here (not in -devel) for pecl command
%{_bindir}/phpize
%{_mandir}/man1/php.1*
%{_mandir}/man1/php-cgi.1*
%{_mandir}/man1/phar.1*
%{_mandir}/man1/phar.phar.1*
%{_mandir}/man1/phpize.1*
%if %{with zts}
%{_bindir}/zts-php
%{_mandir}/man1/zts-php.1*
%{_mandir}/man1/zts-phpize.1*
%endif

%files dbg
%{_bindir}/phpdbg
%{_mandir}/man1/phpdbg.1*
%if %{with zts}
%{_bindir}/zts-phpdbg
%{_mandir}/man1/zts-phpdbg.1*
%endif
%doc sapi/phpdbg/CREDITS

%files fpm
%doc php-fpm.conf.default www.conf.default
%license fpm_LICENSE
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/wsdlcache
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/opcache
%if %{with_httpd2410}
%config(noreplace) %{_httpd_confdir}/php.conf
%else
%doc _fpmdoc/*
%endif
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/php-fpm
%if 0%{?fedora} < 26 && 0%{?rhel} < 8
%config(noreplace) %{_sysconfdir}/sysconfig/php-fpm
%endif
%if %{with_nginx}
%config(noreplace) %{_sysconfdir}/nginx/conf.d/php-fpm.conf
%config(noreplace) %{_sysconfdir}/nginx/default.d/php.conf
%endif
%{_unitdir}/php-fpm.service
%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%config(noreplace) %{_sysconfdir}/systemd/system/httpd.service.d/php-fpm.conf
%config(noreplace) %{_sysconfdir}/systemd/system/nginx.service.d/php-fpm.conf
%endif
%dir %{_sysconfdir}/systemd/system/php-fpm.service.d
%dir %ghost /run/php-fpm
%{_sbindir}/php-fpm
%dir %{_sysconfdir}/php-fpm.d
# log owned by apache for log
%attr(770,apache,root) %dir %{_localstatedir}/log/php-fpm
%{_mandir}/man8/php-fpm.8*
%dir %{_datadir}/fpm
%{_datadir}/fpm/status.html

%if %{with lsws}
%files litespeed
%{_bindir}/lsphp
%endif

%files devel
%{_bindir}/php-config
%{_includedir}/php
%{_libdir}/php/build
%if %{with zts}
%{_bindir}/zts-php-config
%{_includedir}/php-zts
%{_bindir}/zts-phpize
%{_libdir}/php-zts/build
%{_mandir}/man1/zts-php-config.1*
%endif
%{_mandir}/man1/php-config.1*
%{macrosdir}/macros.php

%files embedded
%{_libdir}/libphp.so
%{_libdir}/libphp-%{embed_version}.so

%files pgsql -f files.pgsql
%files odbc -f files.odbc
%if %{with imap}
%files imap -f files.imap
%endif
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files mbstring -f files.mbstring
%license libmbfl_LICENSE
%files gd -f files.gd
%files soap -f files.soap
%files bcmath -f files.bcmath
%license libbcmath_LICENSE
%files gmp -f files.gmp
%files dba -f files.dba
%files pdo -f files.pdo
%files tidy -f files.tidy
%files pdo-dblib -f files.pdo_dblib
%files pspell -f files.pspell
%files intl -f files.intl
%files process -f files.process
%if %{with firebird}
%files pdo-firebird -f files.pdo_firebird
%endif
%files enchant -f files.enchant
%files mysqlnd -f files.mysqlnd
%files opcache -f files.opcache
%config(noreplace) %{_sysconfdir}/php.d/opcache-default.blacklist
%if %{with zts}
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache-default.blacklist
%endif
%if %{with oci8}
%files oci8 -f files.oci8
%endif
%if %{with zip}
%files zip -f files.zip
%endif
%files sodium -f files.sodium
%files ffi -f files.ffi
%dir %{_datadir}/php/preload


%changelog
* Wed Oct 21 2026 Remi Collet <remi@remirepo.net> - 8.0.30-21
- Mitigation fix Avoid state corruption via bailout
  CVE-2026-109618, CVE-2026-109619

* Fri Oct 16 2026 Remi Collet <remi@remirepo.net> - 8.0.30-20
- Fix Out-of-bounds read in the HTTP stream wrapper when following a redirect with an empty Location header
  CVE-2026-93682

* Thu Oct  1 2026 Remi Collet <remi@remirepo.net> - 8.0.30-19
- Fix FILTER_SANITIZE_ENCODED does not encode 0xFF
- Fix IPv6 ACL bypass in FastCGI listen.allowed_clients due to partial address comparison
  CVE-2026-91768
- Fix Various packet overreads in mysqlnd wire protocol
  CVE-2025-1218
- Fix TLS hostname verification falls back to CN after SAN mismatch
  CVE-2026-91769
- Fix Heap buffer overflow in php_openssl_matches_wildcard_name() on crafted server certificate wildcard CN
  CVE-2026-91767
- Fix Integer overflow in phar_tar_number() allowing TAR archive entry injection
  CVE-2026-6103
- Fix Unbounded recursion in server-side cleanup_xml_node()
  CVE-2026-91765
- Fix Integer overflow to buffer overflow in SOAP HTTP parsing
  CVE-2025-14181
- Fix Out-of-bounds read in convert.* stream filters when line-break-chars contains NUL
  CVE-2026-92842
- Fix Cross-origin credential leak in HTTP stream wrapper redirects
  CVE-2026-91766

* Thu Jul 30 2026 Remi Collet <remi@remirepo.net> - 8.0.30-18
- Fix leak on double DatePeriod::__construct() call
- Fixed SQL injection via E'...' backslash breakout
  CVE-2026-17543
- Fixed GHSA-vc5h-9ppw-p5f3 Crash via recursive symlinks
  CVE-2026-7260

* Wed Jul  1 2026 Remi Collet <remi@remirepo.net> - 8.0.30-17
- Fix Memory corruption (zend_mm_heap corrupted) in openssl_encrypt with AES-WRAP-PAD
  CVE-2026-14355

* Mon May 11 2026 Remi Collet <remi@remirepo.net> - 8.0.30-16
- Fix XSS within status endpoint
  CVE-2026-6735
- Fix Null pointer dereference in php_mb_check_encoding() via mb_ereg_search_init()
  CVE-2026-7259
- Fix SQL injection via NUL bytes in quoted strings
  CVE-2025-14179
- Fix Stale SOAP_GLOBAL(ref_map) pointer with Apache Map
  CVE-2026-6722
- Fix Use-after-free after header parsing failure with SOAP_PERSISTENCE_SESSION
  CVE-2026-7261
- Fix Broken Apache map value NULL check
  CVE-2026-7262
- Fix Signed integer overflow of char array offset
  CVE-2026-7568
- Fix Consistently pass unsigned char to ctype.h functions
  CVE-2026-7258

* Thu Dec 18 2025 Remi Collet <remi@remirepo.net> - 8.0.30-15
- Fix Null byte termination in dns_get_record()
  GHSA-www2-q4fc-65wf
- Fix Heap buffer overflow in array_merge()
  CVE-2025-14178
- Fix Information Leak of Memory in getimagesize
  CVE-2025-14177

* Thu Jul  3 2025 Remi Collet <remi@remirepo.net> - 8.0.30-14
- Fix pgsql extension does not check for errors during escaping
  CVE-2025-1735
- Fix NULL Pointer Dereference in PHP SOAP Extension via Large XML Namespace Prefix
  CVE-2025-6491
- Fix Null byte termination in hostnames
  CVE-2025-1220

* Thu Mar 13 2025 Remi Collet <remi@remirepo.net> - 8.0.30-13
- Fix libxml streams use wrong `content-type` header when requesting a redirected resource
  CVE-2025-1219
- Fix Stream HTTP wrapper header check might omit basic auth header
  CVE-2025-1736
- Fix Stream HTTP wrapper truncate redirect location to 1024 bytes
  CVE-2025-1861
- Fix Streams HTTP wrapper does not fail for headers without colon
  CVE-2025-1734
- Fix Header parser of `http` stream wrapper does not handle folded headers
  CVE-2025-1217
- use oracle client library version 23.7 on x86_64 and aarch64

* Thu Feb 13 2025 Remi Collet <remi@remirepo.net> - 8.0.30-12
- backport fix for ICU 74+
- backport fix strict prototypes

* Wed Nov 27 2024 Remi Collet <remi@remirepo.net> - 8.0.30-11
- Fix Leak partial content of the heap through heap buffer over-read
  CVE-2024-8929

* Fri Nov 22 2024 Remi Collet <remi@remirepo.net> - 8.0.30-10
- Fix Heap-Use-After-Free in sapi_read_post_data Processing in CLI SAPI Interface
  GHSA-4w77-75f9-2c8w
- Fix OOB access in ldap_escape
  CVE-2024-8932
- Fix Integer overflow in the dblib/firebird quoter causing OOB writes
  CVE-2024-11236
- Fix Configuring a proxy in a stream context might allow for CRLF injection in URIs
  CVE-2024-11234
- Fix Single byte overread with convert.quoted-printable-decode filter
  CVE-2024-11233

* Thu Sep 26 2024 Remi Collet <remi@remirepo.net> - 8.0.30-9
- Fix Bypass of CVE-2012-1823, Argument Injection in PHP-CGI
  CVE-2024-4577
- Fix Bypass of CVE-2024-4577, Parameter Injection Vulnerability
  CVE-2024-8926
- Fix cgi.force_redirect configuration is bypassable due to the environment variable collision
  CVE-2024-8927
- Fix Logs from childrens may be altered
  CVE-2024-9026
- Fix Erroneous parsing of multipart form data
  CVE-2024-8925
- use ICU 74.2

* Mon Aug 26 2024 Remi Collet <remi@remirepo.net> - 8.0.30-8
- add backport for https://bugs.php.net/79589
  error:14095126:SSL routines:ssl3_read_n:unexpected eof while reading

* Wed Jul 31 2024 Remi Collet <remi@remirepo.net> - 8.0.30-7
- use oracle client library version 23.5 on x86_64

* Tue Jun  4 2024 Remi Collet <remi@remirepo.net> - 8.0.30-6
- Fix filter bypass in filter_var FILTER_VALIDATE_URL
  CVE-2024-5458

* Wed Apr 10 2024 Remi Collet <remi@remirepo.net> - 8.0.30-5
- Fix __Host-/__Secure- cookie bypass due to partial CVE-2022-31629 fix
  CVE-2024-2756
- Fix password_verify can erroneously return true opening ATO risk
  CVE-2024-3096

* Wed Mar  6 2024 Remi Collet <remi@remirepo.net> - 8.0.30-4
- use oracle client library version 21.13 on x86_64
- patch test suite for zlib-ng
- add EOL message

* Tue Dec 12 2023 Remi Collet <remi@remirepo.net> - 8.0.30-3
- use ICU 73.2
- use oracle client library version 21.12 on x86_64, 19.19 on aarch64
- add fixes for libxml 2.11 and 2.12 from 8.1

* Thu Sep 21 2023 Remi Collet <remi@remirepo.net> - 8.0.30-2
- use oracle client library version 21.11 on x86_64, 19.19 on aarch64
- use official Oracle Instant Client RPM

* Thu Aug  3 2023 Remi Collet <remi@remirepo.net> - 8.0.30-1
- Update to 8.0.30 - http://www.php.net/releases/8_0_30.php
- move httpd/nginx wants directive to config files in /etc

* Thu Jun  8 2023 Remi Collet <remi@remirepo.net> - 8.0.29-1
- Update to 8.0.29 - http://www.php.net/releases/8_0_29.php

* Thu May 11 2023 Remi Collet <remi@remirepo.net> - 8.0.28-4
- define %%__phpize and %%__phpconfig

* Fri Apr 21 2023 Remi Collet <remi@remirepo.net> - 8.0.28-3
- use ICU 72.1
- use oracle client library version 21.10
- fix missing TZData version in intl phpinfo
- fix possible buffer overflow in date

* Tue Feb 21 2023 Remi Collet <remi@remirepo.net> - 8.0.28-2
- F38: enable imap extension

* Tue Feb 14 2023 Remi Collet <remi@remirepo.net> - 8.0.28-1
- Update to 8.0.28 - http://www.php.net/releases/8_0_28.php
- add dependency on pcre2 minimal version

* Fri Feb 10 2023 Remi Collet <remi@remirepo.net> - 8.0.27-2
- F38: disable imap extension

* Tue Jan  3 2023 Remi Collet <remi@remirepo.net> - 8.0.27-1
- Update to 8.0.27 - http://www.php.net/releases/8_0_27.php
- use oracle client library version 21.8

* Wed Nov 23 2022 Remi Collet <remi@remirepo.net> - 8.0.26-1
- Update to 8.0.26 - http://www.php.net/releases/8_0_26.php

* Wed Nov  9 2022 Remi Collet <remi@remirepo.net> - 8.0.26~RC1-1
- update to 8.0.26RC1

* Tue Oct 25 2022 Remi Collet <remi@remirepo.net> - 8.0.25-1
- Update to 8.0.25 - http://www.php.net/releases/8_0_25.php

* Tue Oct 11 2022 Remi Collet <remi@remirepo.net> - 8.0.25~RC1-1
- update to 8.0.25RC1

* Wed Sep 28 2022 Remi Collet <remi@remirepo.net> - 8.0.24-1
- Update to 8.0.24 - http://www.php.net/releases/8_0_24.php

* Wed Sep 14 2022 Remi Collet <remi@remirepo.net> - 8.0.24~RC1-1
- update to 8.0.24RC1

* Tue Aug 30 2022 Remi Collet <remi@remirepo.net> - 8.0.23-1
- Update to 8.0.23 - http://www.php.net/releases/8_0_23.php

* Wed Aug 17 2022 Remi Collet <remi@remirepo.net> - 8.0.23~RC1-1
- update to 8.0.23RC1
- use oracle client library version 21.7
- use ICU 71.1

* Tue Aug  2 2022 Remi Collet <remi@remirepo.net> - 8.0.22-1
- Update to 8.0.22 - http://www.php.net/releases/8_0_22.php

* Fri Jul 29 2022 Remi Collet <remi@remirepo.net> - 8.0.22~RC1-2
- fix snmp backport

* Tue Jul 19 2022 Remi Collet <remi@remirepo.net> - 8.0.22~RC1-1
- update to 8.0.22RC1

* Wed Jul  6 2022 Remi Collet <remi@remirepo.net> - 8.0.21-2
- Update to 8.0.21 - http://www.php.net/releases/8_0_21.php
- rebuild with new sources

* Tue Jul  5 2022 Remi Collet <remi@remirepo.net> - 8.0.21-1
- Update to 8.0.21 - http://www.php.net/releases/8_0_21.php

* Tue Jun 21 2022 Remi Collet <remi@remirepo.net> - 8.0.21~RC1-1
- update to 8.0.21RC1

* Wed Jun  8 2022 Remi Collet <remi@remirepo.net> - 8.0.20-1
- Update to 8.0.20 - http://www.php.net/releases/8_0_20.php

* Fri Jun  3 2022 Remi Collet <remi@remirepo.net> - 8.0.20~RC1-2
- add upstream patch to initialize pcre before mbstring

* Wed May 25 2022 Remi Collet <remi@remirepo.net> - 8.0.20~RC1-1
- update to 8.0.20RC1

* Tue May 10 2022 Remi Collet <remi@remirepo.net> - 8.0.19-1
- Update to 8.0.19 - http://www.php.net/releases/8_0_19.php
- use oracle client library version 21.6

* Tue Apr 26 2022 Remi Collet <remi@remirepo.net> - 8.0.19~RC1-1
- update to 8.0.19RC1

* Wed Apr 13 2022 Remi Collet <remi@remirepo.net> - 8.0.18-1
- Update to 8.0.18 - http://www.php.net/releases/8_0_18.php

* Thu Mar 31 2022 Remi Collet <remi@remirepo.net> - 8.0.18~RC1-1
- update to 8.0.18RC1

* Tue Mar 15 2022 Remi Collet <remi@remirepo.net> - 8.0.17-1
- Update to 8.0.17 - http://www.php.net/releases/8_0_17.php
- retrieve tzdata version

* Wed Mar  2 2022 Remi Collet <remi@remirepo.net> - 8.0.17~RC1-1
- update to 8.0.17RC1

* Tue Feb 22 2022 Remi Collet <remi@remirepo.net> - 8.0.16-2
- retrieve tzdata version
- use oracle client library version 21.5

* Wed Feb 16 2022 Remi Collet <remi@remirepo.net> - 8.0.16-1
- Update to 8.0.16 - http://www.php.net/releases/8_0_16.php

* Thu Feb  3 2022 Remi Collet <remi@remirepo.net> - 8.0.16~RC1-1
- update to 8.0.16RC1

* Tue Jan 18 2022 Remi Collet <remi@remirepo.net> - 8.0.15-1
- Update to 8.0.15 - http://www.php.net/releases/8_0_15.php

* Wed Jan  5 2022 Remi Collet <remi@remirepo.net> - 8.0.15~RC1-1
- update to 8.0.15RC1

* Thu Dec 16 2021 Remi Collet <remi@remirepo.net> - 8.0.14-1
- Update to 8.0.14 - http://www.php.net/releases/8_0_14.php

* Thu Dec  2 2021 Remi Collet <remi@remirepo.net> - 8.0.14~RC1-2
- ensure we use libgd >= 2.3

* Thu Dec  2 2021 Remi Collet <remi@remirepo.net> - 8.0.14~RC1-1
- update to 8.0.14RC1
- use oracle client library version 21.4

* Wed Nov 17 2021 Remi Collet <remi@remirepo.net> - 8.0.13-1
- Update to 8.0.13 - http://www.php.net/releases/8_0_13.php

* Wed Nov  3 2021 Remi Collet <remi@remirepo.net> - 8.0.13~RC1-1
- update to 8.0.13RC1
- dba: enable qdbm backend
- dba: drop gdbm backend

* Tue Oct 26 2021 Remi Collet <remi@remirepo.net> - 8.0.12-2
- add patch for OpenSSL 3.0 on F36 and EL9

* Tue Oct 19 2021 Remi Collet <remi@remirepo.net> - 8.0.12-1
- Update to 8.0.12 - http://www.php.net/releases/8_0_12.php

* Mon Oct 18 2021 Remi Collet <remi@remirepo.net> - 8.0.12~RC1-2
- build using system libxcrypt (Fedora)

* Wed Oct  6 2021 Remi Collet <remi@remirepo.net> - 8.0.12~RC1-1
- update to 8.0.12RC1
- use libicu version 69

* Wed Sep 22 2021 Remi Collet <remi@remirepo.net> - 8.0.11-1
- Update to 8.0.11 - http://www.php.net/releases/8_0_11.php

* Tue Sep  7 2021 Remi Collet <remi@remirepo.net> - 8.0.11~RC1-1
- update to 8.0.11RC1
- use oracle client library version 21.3

* Tue Aug 24 2021 Remi Collet <remi@remirepo.net> - 8.0.10-1
- Update to 8.0.10 - http://www.php.net/releases/8_0_10.php

* Wed Aug 11 2021 Remi Collet <remi@remirepo.net> - 8.0.10~RC1-2
- phar: switch to sha256 signature by default, backported from 8.1
- phar: implement openssl_256 and openssl_512 for signatures, backported from 8.1
- snmp: add sha256 / sha512 security protocol, backported from 8.1

* Tue Aug 10 2021 Remi Collet <remi@remirepo.net> - 8.0.10~RC1-1
- update to 8.0.10RC1
- adapt systzdata patch for timelib 2020.03 (v20)

* Thu Jul 29 2021 Remi Collet <remi@remirepo.net> - 8.0.9-1
- Update to 8.0.9 - http://www.php.net/releases/8_0_9.php

* Tue Jul 13 2021 Remi Collet <remi@remirepo.net> - 8.0.9~RC1-1
- update to 8.0.9RC1

* Tue Jun 29 2021 Remi Collet <remi@remirepo.net> - 8.0.8-1
- Update to 8.0.8 - http://www.php.net/releases/8_0_8.php

* Tue Jun 15 2021 Remi Collet <remi@remirepo.net> - 8.0.8~RC1-1
- update to 8.0.8RC1
- ignore unsupported "threads" option on password_hash

* Wed Jun  2 2021 Remi Collet <remi@remirepo.net> - 8.0.7-1
- Update to 8.0.7 - http://www.php.net/releases/8_0_7.php

* Thu May 20 2021 Remi Collet <remi@remirepo.net> - 8.0.7~RC1-1
- update to 8.0.7RC1

* Sat May  8 2021 Remi Collet <remi@remirepo.net> - 8.0.6-2
- get rid of inet_ntoa, inet_aton, inet_addr and gethostbyaddr calls

* Wed May  5 2021 Remi Collet <remi@remirepo.net> - 8.0.6-1
- Update to 8.0.6 - http://www.php.net/releases/8_0_6.php

* Tue Apr 27 2021 Remi Collet <remi@remirepo.net> - 8.0.5-1
- Update to 8.0.5 - http://www.php.net/releases/8_0_5.php

* Tue Apr 13 2021 Remi Collet <remi@remirepo.net> - 8.0.5~RC1-1
- update to 8.0.5RC1

* Tue Mar 16 2021 Remi Collet <remi@remirepo.net> - 8.0.4~RC1-1
- update to 8.0.4RC1
- use oracle client library version 21.1

* Wed Mar  3 2021 Remi Collet <remi@remirepo.net> - 8.0.3-1
- Update to 8.0.3 - http://www.php.net/releases/8_0_3.php

* Thu Feb 18 2021 Remi Collet <remi@remirepo.net> - 8.0.3~RC1-1
- update to 8.0.3RC1

* Tue Feb  2 2021 Remi Collet <remi@remirepo.net> - 8.0.2-1
- Update to 8.0.2 - http://www.php.net/releases/8_0_2.php

* Thu Jan 28 2021 Remi Collet <remi@remirepo.net> - 8.0.2~RC1-2
- add upstream patch for https://bugs.php.net/80682
  fix opcache doesn't honour pcre.jit option

* Tue Jan 19 2021 Remi Collet <remi@remirepo.net> - 8.0.2~RC1-1
- update to 8.0.2RC1
- oci8 version is now 3.0.1

* Tue Jan  5 2021 Remi Collet <remi@remirepo.net> - 8.0.1-1
- Update to 8.0.1 - http://www.php.net/releases/8_0_1.php

* Tue Dec 15 2020 Remi Collet <remi@remirepo.net> - 8.0.1~RC1-1
- update to 8.0.1RC1

* Wed Nov 25 2020 Remi Collet <remi@remirepo.net> - 8.0.0-1
- update to 8.0.0 GA

* Wed Nov 18 2020 Remi Collet <remi@remirepo.net> - 8.0.0~rc5-9
- update to 8.0.0RC5
- use oracle client library version 19.9

* Tue Nov 10 2020 Remi Collet <remi@remirepo.net> - 8.0.0~rc4-8
- update to 8.0.0RC4

* Tue Oct 27 2020 Remi Collet <remi@remirepo.net> - 8.0.0~rc3-7
- update to 8.0.0RC3

* Wed Oct 14 2020 Remi Collet <remi@remirepo.net> - 8.0.0~rc2-6
- update to 8.0.0RC2

* Wed Sep 30 2020 Remi Collet <remi@remirepo.net> - 8.0.0~rc1-34
- update to 8.0.0rc1
- bump ABI/API versions

* Thu Sep 17 2020 Remi Collet <remi@remirepo.net> - 8.0.0~beta4-4
- drop mod_php for ZTS (have never be suported)
- use %%bcond_without for dtrace, libgd, firebird, lsws, libpcre and zts
  so can be disabled during rebuild
- use %%bcond_with for libgd, libpcre, oci8, zip and debug
  so can be enabled during rebuild

* Thu Sep 17 2020 Remi Collet <remi@remirepo.net> - 8.0.0~beta4-3
- properly use --enable-zts for ZTS builds

* Wed Sep 16 2020 Remi Collet <remi@remirepo.net> - 8.0.0~beta4-2
- update to 8.0.0beta4

* Fri Sep 11 2020 Remi Collet <remi@remirepo.net> - 8.0.0~beta3-1
- update to 8.0.0beta3
- bump ABI/API versions
- drop xmlrpc extension
- json is now build statically
- use system nikic/php-parser if available to generate
  C headers from PHP stub
- switch from "runselftest" option to %bcond_without tests
- enchant: use libenchant-2 instead of libenchant
- rename 15-php.conf to 20-php.conf to ensure load order
- oci8 version is now 3.0.0

* Tue Sep  1 2020 Remi Collet <remi@remirepo.net> - 7.4.10-1
- Update to 7.4.10 - http://www.php.net/releases/7_4_10.php

* Tue Aug 18 2020 Remi Collet <remi@remirepo.net> - 7.4.10~RC1-1
- update to 7.4.10RC1
- use oracle client library version 19.8 (x86_64)

* Tue Aug  4 2020 Remi Collet <remi@remirepo.net> - 7.4.9-1
- Update to 7.4.9 - http://www.php.net/releases/7_4_9.php

* Tue Jul 21 2020 Remi Collet <remi@remirepo.net> - 7.4.9~RC1-1
- update to 7.4.9RC1
- build using ICU 65

* Thu Jul  9 2020 Remi Collet <remi@remirepo.net> - 7.4.8-2
- Update to 7.4.8 - http://www.php.net/releases/7_4_8.php
  rebuild from new sources

* Tue Jul  7 2020 Remi Collet <remi@remirepo.net> - 7.4.8-1
- Update to 7.4.8 - http://www.php.net/releases/7_4_8.php

* Mon Jul  6 2020 Remi Collet <remi@remirepo.net> - 7.4.8~RC1-2
- display build system and provider in phpinfo (from 8.0)

* Tue Jun 23 2020 Remi Collet <remi@remirepo.net> - 7.4.8~RC1-1
- update to 7.4.8RC1
- drop patch to fix PHP_UNAME

* Tue Jun  9 2020 Remi Collet <remi@remirepo.net> - 7.4.7-1
- Update to 7.4.7 - http://www.php.net/releases/7_4_7.php
- rebuild using oniguruma5php
- build phpdbg only once

* Tue May 26 2020 Remi Collet <remi@remirepo.net> - 7.4.7~RC1-1
- update to 7.4.7RC1

* Wed May 20 2020 Remi Collet <remi@remirepo.net> - 7.4.6-2
- use php-config from embed SAPI to reduce used libs

* Tue May 12 2020 Remi Collet <remi@remirepo.net> - 7.4.6-1
- Update to 7.4.6 - http://www.php.net/releases/7_4_6.php

* Wed Apr 29 2020 Remi Collet <remi@remirepo.net> - 7.4.6~RC1-1
- update to 7.4.6RC1

* Tue Apr 14 2020 Remi Collet <remi@remirepo.net> - 7.4.5-1
- Update to 7.4.5 - http://www.php.net/releases/7_4_5.php

* Tue Mar 31 2020 Remi Collet <remi@remirepo.net> - 7.4.5~RC1-1
- update to 7.4.5RC1

* Tue Mar 17 2020 Remi Collet <remi@remirepo.net> - 7.4.4-1
- Update to 7.4.4 - http://www.php.net/releases/7_4_4.php
- use oracle client library version 19.6 (18.5 on EL-6)

* Tue Mar  3 2020 Remi Collet <remi@remirepo.net> - 7.4.4~RC1-1
- update to 7.4.4RC1

* Tue Feb 18 2020 Remi Collet <remi@remirepo.net> - 7.4.3-1
- Update to 7.4.3 - http://www.php.net/releases/7_4_3.php

* Tue Feb  4 2020 Remi Collet <remi@remirepo.net> - 7.4.3~RC1-1
- update to 7.4.3RC1

* Tue Jan 28 2020 Remi Collet <remi@remirepo.net> - 7.4.2-2
- make sodium mandatory on EL-7, to avoid user confusion
  https://github.com/remicollet/remirepo/issues/137

* Tue Jan 21 2020 Remi Collet <remi@remirepo.net> - 7.4.2-1
- Update to 7.4.2 - http://www.php.net/releases/7_4_2.php

* Tue Jan  7 2020 Remi Collet <remi@remirepo.net> - 7.4.2~RC1-1
- update to 7.4.2RC1

* Wed Dec 18 2019 Remi Collet <remi@remirepo.net> - 7.4.1-1
- Update to 7.4.1 - http://www.php.net/releases/7_4_1.php

* Wed Dec 11 2019 Remi Collet <remi@remirepo.net> - 7.4.1~RC1-1
- update to 7.4.1RC1
- use oracle client library version 19.5

* Wed Nov 27 2019 Remi Collet <remi@remirepo.net> - 7.4.0-1
- update to 7.4.0 GA

* Mon Nov 11 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC6-15
- update to 7.4.0RC6

* Tue Oct 29 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC5-14
- update to 7.4.0RC5
- set opcache.enable_cli in provided default configuration

* Fri Oct 25 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC4-13
- add /usr/share/php/preload as default ffi.preload configuration

* Thu Oct 24 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC4-12
- allow wildcards in ffi.preload

* Wed Oct 23 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC4-11
- fix preload, add more upstream patches for #78713 #78716

* Mon Oct 21 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC4-10
- fix preload, add upstream patch for #78512
- change dependency on nginx-filesystem to weak

* Tue Oct 15 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC4-9
- update to 7.4.0RC4

* Thu Oct 10 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC3-8
- fix librt issue on F31 using upstream patch

* Mon Oct  7 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC3-7
- ensure all shared extensions can be loaded

* Fri Oct  4 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC3-6
- fix broken intl extension on EL-7

* Tue Oct  1 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC3-5
- update to 7.4.0RC3

* Fri Sep 20 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC2-4
- fix broken gmp extension https://bugs.php.net/78574

* Tue Sep 17 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC2-3
- update to 7.4.0RC2 (new tag)

* Tue Sep 17 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC2-2
- update to 7.4.0RC2
- add tarball signature check
- reduce to 4 concurrent test workers

* Thu Sep  5 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC1-1
- update to 7.4.0RC1

* Wed Aug 28 2019 Remi Collet <remi@remirepo.net> - 7.3.9-1
- Update to 7.3.9 - http://www.php.net/releases/7_3_9.php

* Mon Aug 19 2019 Remi Collet <remi@remirepo.net> - 7.3.9~RC1-1
- update to 7.3.9RC1

* Tue Jul 30 2019 Remi Collet <remi@remirepo.net> - 7.3.8-1
- Update to 7.3.8 - http://www.php.net/releases/7_3_8.php

* Tue Jul 16 2019 Remi Collet <remi@remirepo.net> - 7.3.8~RC1-1
- update to 7.3.8RC1
- add upstream patch for #78297
- main package now recommends commonly used extensions
  (json, mbstring, opcache, pdo, xml)

* Wed Jul  3 2019 Remi Collet <remi@remirepo.net> - 7.3.7-3
- rebuild 7.3.7 (new tag)

* Wed Jul  3 2019 Remi Collet <remi@remirepo.net> - 7.3.7-2
- add upstream patch for https://bugs.php.net/78230
  segfault with opcache enabled

* Tue Jul  2 2019 Remi Collet <remi@remirepo.net> - 7.3.7-1
- Update to 7.3.7 - http://www.php.net/releases/7_3_7.php
- disable opcache.huge_code_pages in default configuration

* Thu Jun 20 2019 Remi Collet <remi@remirepo.net> - 7.3.7~RC3-1
- update to 7.3.7RC3

* Tue Jun 18 2019 Remi Collet <remi@remirepo.net> - 7.3.7~RC2-1
- update to 7.3.7RC2

* Mon Jun 17 2019 Remi Collet <remi@remirepo.net> - 7.3.7~RC1-2
- use oracle client library version 19.3

* Tue Jun 11 2019 Remi Collet <remi@remirepo.net> - 7.3.7~RC1-1
- update to 7.3.7RC1

* Tue May 28 2019 Remi Collet <remi@remirepo.net> - 7.3.6-3
- Update to 7.3.6 - http://www.php.net/releases/7_3_6.php

* Thu May 16 2019 Remi Collet <remi@remirepo.net> - 7.3.6~RC1-3
- add httpd and nginx configuration files for FPM in documentation

* Wed May 15 2019 Remi Collet <remi@remirepo.net> - 7.3.6~RC1-2
- update to 7.3.6RC1 (new tag)

* Tue May 14 2019 Remi Collet <remi@remirepo.net> - 7.3.6~RC1-1
- update to 7.3.6RC1

* Wed May  1 2019 Remi Collet <remi@remirepo.net> - 7.3.5-1
- Update to 7.3.5 - http://www.php.net/releases/7_3_5.php

* Tue Apr 16 2019 Remi Collet <remi@remirepo.net> - 7.3.5~RC1-1
- update to 7.3.5RC1

* Fri Apr  5 2019 Remi Collet <remi@remirepo.net> - 7.3.4-2
- build with system oniguruma5

* Tue Apr  2 2019 Remi Collet <remi@remirepo.net> - 7.3.4-1
- Update to 7.3.4 - http://www.php.net/releases/7_3_4.php

* Thu Mar 21 2019 Remi Collet <remi@remirepo.net> - 7.3.4~RC1-2
- update to 7.3.4RC1 new tag
- add upstream patches for failed tests

* Tue Mar 19 2019 Remi Collet <remi@remirepo.net> - 7.3.4~RC1-1
- update to 7.3.4RC1

* Tue Mar  5 2019 Remi Collet <remi@remirepo.net> - 7.3.3-1
- Update to 7.3.3 - http://www.php.net/releases/7_3_3.php
- add upstream patch for OpenSSL 1.1.1b

* Fri Feb 22 2019 Remi Collet <remi@remirepo.net> - 7.3.3~RC1-2
- php-devel: drop dependency on libicu-devel

* Tue Feb 19 2019 Remi Collet <remi@remirepo.net> - 7.3.3~RC1-1
- update to 7.3.3RC1
- adapt systzdata patch (v18)

* Mon Feb 18 2019 Remi Collet <remi@remirepo.net> - 7.3.2-2
- pdo_oci: backport PDOStatement::getColumnMeta from 7.4
- rebuild using libicu62
- drop configuration for ZTS mod_php (Fedora >= 27)

* Wed Feb  6 2019 Remi Collet <remi@remirepo.net> - 7.3.2-1
- Update to 7.3.2 - http://www.php.net/releases/7_3_2.php

* Tue Jan 22 2019 Remi Collet <remi@remirepo.net> - 7.3.2~RC1-1
- update to 7.3.2RC1
- update system tzdata patch for timelib 2018.01

* Tue Jan  8 2019 Remi Collet <remi@remirepo.net> - 7.3.1-1
- Update to 7.3.1 - http://www.php.net/releases/7_3_1.php

* Tue Dec 18 2018 Remi Collet <remi@remirepo.net> - 7.3.1~RC1-1
- update to 7.3.1RC1
- oci8 version is now 2.1.8

* Tue Dec  4 2018 Remi Collet <remi@remirepo.net> - 7.3.0-1
- update to 7.3.0 GA
- update FPM configuration from upstream

* Fri Nov 30 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc6-2
- EL-8 build

* Tue Nov 20 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc6-1
- update to 7.3.0RC6

* Tue Nov  6 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc5-1
- update to 7.3.0RC5

* Wed Oct 24 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc4-1
- update to 7.3.0RC4

* Tue Oct  9 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc3-1
- update to 7.3.0RC3

* Tue Sep 25 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc2-1
- update to 7.3.0RC2
- use oracle client library version 18.3

* Tue Sep 11 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc1-1
- update to 7.3.0RC1
- with oniguruma 6.9.0

* Tue Aug 28 2018 Remi Collet <remi@remirepo.net> - 7.3.0~beta3-1
- update to 7.3.0beta3

* Wed Aug 22 2018 Remi Collet <remi@remirepo.net> - 7.3.0~beta2-2
- drop -mstackrealign option, workaround to #1593144

* Tue Aug 21 2018 Remi Collet <remi@remirepo.net> - 7.3.0~beta2-1
- update to 7.3.0beta2
- bump API numbers

* Wed Aug 15 2018 Remi Collet <remi@remirepo.net> - 7.2.9-1
- Update to 7.2.9 - http://www.php.net/releases/7_2_9.php

* Tue Jul 17 2018 Remi Collet <remi@remirepo.net> - 7.2.8-1
- Update to 7.2.8 - http://www.php.net/releases/7_2_8.php

* Tue Jul  3 2018 Remi Collet <remi@remirepo.net> - 7.2.8~RC1-2
- FPM: add getallheaders, backported from 7.3

* Tue Jul  3 2018 Remi Collet <remi@remirepo.net> - 7.2.8~RC1-1
- update to 7.2.8RC1

* Wed Jun 20 2018 Remi Collet <remi@remirepo.net> - 7.2.7-1
- Update to 7.2.7 - http://www.php.net/releases/7_2_7.php

* Wed Jun  6 2018 Remi Collet <remi@remirepo.net> - 7.2.7~RC1-1
- update to 7.2.7RC1

* Wed May 23 2018 Remi Collet <remi@remirepo.net> - 7.2.6-1
- Update to 7.2.6 - http://www.php.net/releases/7_2_6.php

* Mon May 14 2018 Remi Collet <remi@remirepo.net> - 7.2.6~RC1-2
- rebuild against EL 7.5

* Sun May 13 2018 Remi Collet <remi@remirepo.net> - 7.2.6~RC1-1
- update to 7.2.6RC1

* Tue Apr 24 2018 Remi Collet <remi@remirepo.net> - 7.2.5-1
- Update to 7.2.5 - http://www.php.net/releases/7_2_5.php

* Wed Apr 11 2018 Remi Collet <remi@remirepo.net> - 7.2.5~RC1-1
- update to 7.2.5RC1

* Tue Apr  3 2018 Remi Collet <remi@remirepo.net> - 7.2.4-2
- add upstream patch for oniguruma 6.8.1, FTBFS #1562583

* Tue Mar 27 2018 Remi Collet <remi@remirepo.net> - 7.2.4-1
- Update to 7.2.4 - http://www.php.net/releases/7_2_4.php
- FPM: update default pool configuration for process.dumpable

* Wed Mar 21 2018 Remi Collet <remi@remirepo.net> - 7.2.4~RC1-3
- use systemd RuntimeDirectory instead of /etc/tmpfiles.d

* Thu Mar 15 2018 Remi Collet <remi@remirepo.net> - 7.2.4~RC1-2
- add file trigger to restart the php-fpm service
  when new pool or new extension installed (F27+)

* Tue Mar 13 2018 Remi Collet <remi@remirepo.net> - 7.2.4~RC1-1
- update to 7.2.4RC1

* Fri Mar  2 2018 Remi Collet <remi@remirepo.net> - 7.2.3-2
- devel: drop dependency on devtoolset

* Wed Feb 28 2018 Remi Collet <remi@remirepo.net> - 7.2.3-1
- Update to 7.2.3 - http://www.php.net/releases/7_2_3.php
- FPM: revert pid file removal
- improve devel dependencies

* Wed Feb 14 2018 Remi Collet <remi@remirepo.net> - 7.2.3~RC1-2
- rebuild for new tag and drop patch merged upstream
- drop ldconfig scriptlets on F28

* Wed Feb 14 2018 Remi Collet <remi@remirepo.net> - 7.2.3~RC1-1
- update to 7.2.3RC1
- adapt systzdata, fixheader and ldap_r patches
- apply upstream patch for date ext

* Tue Jan 30 2018 Remi Collet <remi@remirepo.net> - 7.2.2-1
- Update to 7.2.2 - http://www.php.net/releases/7_2_2.php

* Tue Jan 16 2018 Remi Collet <remi@remirepo.net> - 7.2.2~RC1-2
- dba: revert drop gdbm support

* Tue Jan 16 2018 Remi Collet <remi@remirepo.net> - 7.2.2~RC1-1
- update to 7.2.2RC1
- define SOURCE_DATE_EPOCH for reproducible build
- dba: drop gdbm support

* Wed Jan 10 2018 Remi Collet <remi@remirepo.net> - 7.2.1-2
- rebuild for gdbm 1.14 BC break (see rhbz#1532997)

* Wed Jan  3 2018 Remi Collet <remi@remirepo.net> - 7.2.1-1
- Update to 7.2.1 - http://www.php.net/releases/7_2_1.php

* Wed Dec 13 2017 Remi Collet <remi@remirepo.net> - 7.2.1~RC1-1
- update to 7.2.1RC1

* Tue Nov 28 2017 Remi Collet <remi@remirepo.net> - 7.2.0-2
- refresh patch for https://bugs.php.net/75514

* Tue Nov 28 2017 Remi Collet <remi@remirepo.net> - 7.2.0-1
- update to 7.2.0 GA

* Tue Nov  7 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC6-1
- update to 7.2.0RC6

* Tue Oct 24 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC5-1
- update to 7.2.0RC5

* Wed Oct 18 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC4-2
- enable argon2 password hash

* Tue Oct 10 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC4-1
- update to 7.2.0RC4
- oci8 version is now 2.1.8
- dont obsolete php-pecl-libsodium

* Tue Sep 26 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC3-1
- update to 7.2.0RC2

* Mon Sep 25 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC2-3
- F27: php now requires php-fpm and start it with httpd / nginx

* Thu Sep 14 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC2-2
- update builder from RHEL 7.3 to RHEL 7.4

* Wed Sep 13 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC2-1
- update to 7.2.0RC2

* Thu Aug 31 2017 Remi Collet <remi@fedoraproject.org> - 7.2.0~RC1-2
- add patch for EL-6, fix undefined symbol: sqlite3_errstr

* Wed Aug 30 2017 Remi Collet <remi@fedoraproject.org> - 7.2.0~RC1-1
- update to 7.2.0RC1

* Tue Aug 22 2017 Remi Collet <remi@fedoraproject.org> - 7.1.9~RC1-2
- disable httpd MPM check
- php-fpm: drop unneeded "pid" from default configuration

* Wed Aug 16 2017 Remi Collet <remi@fedoraproject.org> - 7.1.9~RC1-1
- Update to 7.1.9RC1
- oci8 version is now 2.1.7

* Wed Aug  2 2017 Remi Collet <remi@fedoraproject.org> - 7.1.8-2
- add patch for EL-6, fix undefined symbol: sqlite3_errstr

* Wed Aug  2 2017 Remi Collet <remi@fedoraproject.org> - 7.1.8-1
- Update to 7.1.8 - http://www.php.net/releases/7_1_8.php

* Tue Jul 18 2017 Remi Collet <remi@fedoraproject.org> - 7.1.8~RC1-1
- Update to 7.1.8RC1
- oci8 version is now 2.1.6

* Thu Jul  6 2017 Remi Collet <remi@fedoraproject.org> - 7.1.7-1
- Update to 7.1.7 - http://www.php.net/releases/7_1_7.php

* Wed Jun 21 2017 Remi Collet <remi@fedoraproject.org> - 7.1.7~RC1-1
- Update to 7.1.7RC1
- oci8 version is now 2.1.5
- use oracle instant client version 12.2

* Wed Jun  7 2017 Remi Collet <remi@fedoraproject.org> - 7.1.6-1
- Update to 7.1.6 - http://www.php.net/releases/7_1_6.php
- add upstream security patches for oniguruma

* Wed May 24 2017 Remi Collet <remi@fedoraproject.org> - 7.1.6~RC1-1
- Update to 7.1.6RC1

* Tue May  9 2017 Remi Collet <remi@fedoraproject.org> - 7.1.5-1
- Update to 7.1.5 - http://www.php.net/releases/7_1_5.php

* Thu Apr 27 2017 Remi Collet <remi@fedoraproject.org> - 7.1.5~RC1-2
- new sources from new tag

* Tue Apr 25 2017 Remi Collet <remi@fedoraproject.org> - 7.1.5~RC1-1
- Update to 7.1.5RC1
- oci8 version is now 2.1.4

* Tue Apr 11 2017 Remi Collet <remi@fedoraproject.org> - 7.1.4-1
- Update to 7.1.4 - http://www.php.net/releases/7_1_4.php

* Tue Mar 28 2017 Remi Collet <remi@fedoraproject.org> - 7.1.4-0.1.RC1
- Update to 7.1.4RC1

* Tue Mar 14 2017 Remi Collet <remi@fedoraproject.org> - 7.1.3-1
- Update to 7.1.3 - http://www.php.net/releases/7_1_3.php

* Fri Mar 10 2017 Remi Collet <remi@fedoraproject.org> - 7.1.3-0.2.RC1
- fix interbase build on F26

* Tue Feb 28 2017 Remi Collet <remi@fedoraproject.org> - 7.1.3-0.1.RC1
- Update to 7.1.3RC1

* Wed Feb 15 2017 Remi Collet <remi@fedoraproject.org> - 7.1.2-1
- Update to 7.1.2 - http://www.php.net/releases/7_1_2.php

* Thu Feb  2 2017 Remi Collet <remi@fedoraproject.org> - 7.1.2-0.2.RC1
- Update to 7.1.2RC1 (new sources)

* Wed Feb  1 2017 Remi Collet <remi@fedoraproject.org> 7.1.2-0.1.RC1
- Update to 7.1.2RC1

* Wed Jan 18 2017 Remi Collet <remi@fedoraproject.org> 7.1.1-3
- EL-7: add patch for https://bugs.php.net/73956
- switch back to gcc 6.2

* Wed Jan 18 2017 Remi Collet <remi@fedoraproject.org> 7.1.1-2
- EL-7: rebuild using gcc 4.8 instead of 6.2
  because of https://bugzilla.redhat.com/1414348

* Wed Jan 18 2017 Remi Collet <remi@fedoraproject.org> 7.1.1-1
- Update to 7.1.1 - http://www.php.net/releases/7_1_1.php

* Thu Jan  5 2017 Remi Collet <remi@fedoraproject.org> 7.1.1-0.1.RC1
- Update to 7.1.1RC1

* Mon Dec 26 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-2
- test optimized build using GCC 6.2

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-1
- Update to 7.1.0 - http://www.php.net/releases/7_1_0.php
- use bundled pcre library 8.38 on EL-7
- disable pcre.jit everywhere as it raise AVC #1398474
- sync provided configuration with upstream production defaults

* Wed Nov  9 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.8.RC6
- Update to 7.1.0RC6

* Wed Oct 26 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.7.RC5
- Update to 7.1.0RC5

* Mon Oct 17 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.6.RC4
- Update to 7.1.0RC4
- update tzdata patch to v14, improve check for valid tz file
- oci8 version is now 2.1.3

* Thu Sep 29 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.5.RC3
- Update to 7.1.0RC3

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.4.RC2
- Update to 7.1.0RC2
- API version is now 20160303

* Thu Sep  1 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.3.RC1
- Update to 7.1.0RC1
- oci8 version is now 2.1.2
- json version is now 1.5.0

* Wed Aug  3 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.2.beta2
- Update to 7.1.0beta2

* Sat Jul 23 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.1.beta1
- Update to 7.1.0beta1

* Wed Jul 20 2016 Remi Collet <remi@fedoraproject.org> 7.0.9-1
- Update to 7.0.9 - http://www.php.net/releases/7_0_9.php
- wddx: add upstream patch for https://bugs.php.net/72564

* Wed Jul  6 2016 Remi Collet <remi@fedoraproject.org> 7.0.9-0.1.RC1
- Update to 7.0.9RC1

* Thu Jun 30 2016 Remi Collet <remi@fedoraproject.org> 7.0.8-1.1
- own tests/doc directories for pecl packages (f24)

* Wed Jun 22 2016 Remi Collet <remi@fedoraproject.org> 7.0.8-1
- Update to 7.0.8 - http://www.php.net/releases/7_0_8.php

* Wed Jun  8 2016 Remi Collet <remi@fedoraproject.org> 7.0.8-0.1.RC1
- Update to 7.0.8RC1
- opcache version is now php version

* Wed May 25 2016 Remi Collet <remi@fedoraproject.org> 7.0.7-1
- Update to 7.0.7 - http://www.php.net/releases/7_0_7.php

* Thu May 12 2016 Remi Collet <remi@fedoraproject.org> 7.0.7-0.1.RC1
- Update to 7.0.7RC1
- oci8 version is now 2.1.1

* Thu Apr 28 2016 Remi Collet <remi@fedoraproject.org> 7.0.6-3
- Update to 7.0.6 - http://www.php.net/releases/7_0_6.php
- rebuild for new sources

* Wed Apr 27 2016 Remi Collet <remi@fedoraproject.org> 7.0.6-1
- Update to 7.0.6
  http://www.php.net/releases/7_0_6.php

* Tue Apr 12 2016 Remi Collet <remi@fedoraproject.org> 7.0.6-0.1.RC1
- Update to 7.0.6RC1

* Fri Apr  8 2016 Remi Collet <remi@fedoraproject.org> 7.0.5-2
- Fixed bug #71914 (Reference is lost in "switch")

* Wed Mar 30 2016 Remi Collet <remi@fedoraproject.org> 7.0.5-1
- Update to 7.0.5
  http://www.php.net/releases/7_0_5.php

* Wed Mar 16 2016 Remi Collet <remi@fedoraproject.org> 7.0.5-0.1.RC1
- Update to 7.0.5RC1

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> 7.0.4-2
- adapt for F24: define %%pecl_xmldir and own it

* Wed Mar  2 2016 Remi Collet <remi@fedoraproject.org> 7.0.4-1
- Update to 7.0.4
  http://www.php.net/releases/7_0_4.php
- pcre: disables JIT compilation of patterns with system pcre < 8.38

* Thu Feb 18 2016 Remi Collet <remi@fedoraproject.org> 7.0.4-0.1.RC1
- Update to 7.0.4RC1

* Wed Feb  3 2016 Remi Collet <remi@fedoraproject.org> 7.0.3-1
- Update to 7.0.3
  http://www.php.net/releases/7_0_3.php

* Fri Jan 29 2016 Remi Collet <remi@fedoraproject.org> 7.0.3-0.2.RC1
- FPM: test build for https://bugs.php.net/62172

* Wed Jan 20 2016 Remi Collet <remi@fedoraproject.org> 7.0.3-0.1.RC1
- Update to 7.0.3RC1

* Wed Jan  6 2016 Remi Collet <remi@fedoraproject.org> 7.0.2-1
- Update to 7.0.2
  http://www.php.net/releases/7_0_2.php

* Sun Dec 27 2015 Remi Collet <remi@fedoraproject.org> 7.0.2-0.1.RC1
- Update to 7.0.2RC1
- opcache: build with --disable-huge-code-pages on EL-6

* Wed Dec 16 2015 Remi Collet <remi@fedoraproject.org> 7.0.1-1
- Update to 7.0.1
  http://www.php.net/releases/7_0_1.php
- curl: add CURL_SSLVERSION_TLSv1_x constant (EL)

* Wed Dec  9 2015 Remi Collet <remi@fedoraproject.org> 7.0.1-0.1.RC1
- Update to 7.0.1RC1
- drop --disable-huge-code-pages build option on EL-6,
  but keep it disabled in default configuration
- php-devel obsoletes php-pecl-jsonc-devel

* Sat Dec  5 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-3
- EL-6 rebuild

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-2
- build with --disable-huge-code-pages on EL-6

* Tue Dec  1 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-1
- Update to 7.0.0
  http://www.php.net/releases/7_0_0.php

* Mon Nov 30 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.16.RC8
- set opcache.huge_code_pages=0 on EL-6
  see  https://bugs.php.net/70973 and https://bugs.php.net/70977

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.12.RC8
- Update to 7.0.0RC8
- set opcache.huge_code_pages=1 on x86_64

* Thu Nov 12 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.11.RC7
- Update to 7.0.0RC7 (retagged)

* Wed Nov 11 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.10.RC7
- Update to 7.0.0RC7

* Wed Oct 28 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.9.RC6
- Update to 7.0.0RC6

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.8.RC5
- rebuild as retagged

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.7.RC5
- Update to 7.0.0RC5
- update php-fpm.d/www.conf comments
- API and Zend API are now set to 20151012

* Wed Sep 30 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.6.RC4
- Update to 7.0.0RC4
- php-fpm: set http authorization headers

* Wed Sep 16 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.5.RC3
- Update to 7.0.0RC3
- disable zip extension (provided in php-pecl-zip)

* Fri Sep  4 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.4.RC2
- Update to 7.0.0RC2
- enable oci8 and pdo_oci extensions
- sync php.ini with upstream php.ini-production

* Sat Aug 22 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.3.RC1
- Update to 7.0.0RC1

* Wed Aug  5 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.2.beta3
- update to 7.0.0beta3

* Thu Jul 23 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.1.beta2
- update to 7.0.0beta2
- merge changes from php70-php spec file

* Sun Jul 12 2015 Remi Collet <remi@fedoraproject.org> 5.6.11-1
- Update to 5.6.11
  http://www.php.net/releases/5_6_11.php

* Thu Jun 11 2015 Remi Collet <remi@fedoraproject.org> 5.6.10-1.1
- don't provide php-sqlite3 on EL-5
- the phar link is now correctly created
- avoid issue when 2 builds run simultaneously

* Thu Jun 11 2015 Remi Collet <remi@fedoraproject.org> 5.6.10-1
- Update to 5.6.10
  http://www.php.net/releases/5_6_10.php
- opcache is now 7.0.6-dev

* Fri May 15 2015 Remi Collet <remi@fedoraproject.org> 5.6.9-1
- Update to 5.6.9
  http://www.php.net/releases/5_6_9.php

* Thu Apr 16 2015 Remi Collet <remi@fedoraproject.org> 5.6.8-1
- Update to 5.6.8
  http://www.php.net/releases/5_6_8.php

* Fri Apr 10 2015 Remi Collet <remi@fedoraproject.org> 5.6.7-2
- add upstream patch to drop SSLv3 tests

* Thu Mar 19 2015 Remi Collet <remi@fedoraproject.org> 5.6.7-1
- Update to 5.6.7
  http://www.php.net/releases/5_6_7.php

* Fri Feb 20 2015 Remi Collet <remi@fedoraproject.org> 5.6.6-1.1
- rebuild for new tokyocabinet in EL-5

* Thu Feb 19 2015 Remi Collet <remi@fedoraproject.org> 5.6.6-1
- Update to 5.6.6
  http://www.php.net/releases/5_6_6.php

* Wed Jan 21 2015 Remi Collet <remi@fedoraproject.org> 5.6.5-1
- Update to 5.6.5
  http://www.php.net/releases/5_6_5.php

* Fri Jan  9 2015 Remi Collet <remi@fedoraproject.org> 5.6.5-0.1.RC1
- update to 5.6.5RC1
- FPM: enable ACL for Unix Domain Socket

* Wed Dec 17 2014 Remi Collet <remi@fedoraproject.org> 5.6.4-2
- Update to 5.6.4
  http://www.php.net/releases/5_6_4.php
- add sybase_ct extension (in mssql sub-package)
- xmlrpc requires xml

* Wed Dec 10 2014 Remi Collet <remi@fedoraproject.org> 5.6.4-1
- Update to 5.6.4
  http://www.php.net/releases/5_6_4.php

* Thu Nov 27 2014 Remi Collet <rcollet@redhat.com> 5.6.4-0.1.RC1
- php 5.6.4RC1

* Sun Nov 16 2014 Remi Collet <remi@fedoraproject.org> 5.6.3-3
- FPM: add upstream patch for https://bugs.php.net/68421
  access.format=R doesn't log ipv6 address
- FPM: add upstream patch for https://bugs.php.net/68420
  listen=9000 listens to ipv6 localhost instead of all addresses
- FPM: add upstream patch for https://bugs.php.net/68423
  will no longer load all pools

* Thu Nov 13 2014 Remi Collet <remi@fedoraproject.org> 5.6.3-1
- Update to PHP 5.6.3
  http://php.net/releases/5_6_3.php
- GMP: add upstream patch for https://bugs.php.net/68419
  Fix build with libgmp < 4.2

* Thu Oct 30 2014 Remi Collet <rcollet@redhat.com> 5.6.3-0.4.RC1
- php 5.6.3RC1 (refreshed, phpdbg changes reverted)

* Thu Oct 30 2014 Remi Collet <rcollet@redhat.com> 5.6.3-0.3.RC1
- new version of systzdata patch, fix case sensitivity
- ignore Factory in date tests

* Wed Oct 29 2014 Remi Collet <rcollet@redhat.com> 5.6.3-0.2.RC1
- php 5.6.3RC1 (refreshed)
- enable phpdbg_webhelper new extension (in php-dbg)

* Tue Oct 28 2014 Remi Collet <rcollet@redhat.com> 5.6.3-0.1.RC1
- php 5.6.3RC1
- disable opcache.fast_shutdown in default config
- disable phpdbg_webhelper new extension for now

* Thu Oct 16 2014 Remi Collet <remi@fedoraproject.org> 5.6.1-1
- Update to PHP 5.6.2
  http://php.net/releases/5_6_2.php

* Fri Oct  3 2014 Remi Collet <remi@fedoraproject.org> 5.6.1-1
- Update to PHP 5.6.1
  http://php.net/releases/5_6_1.php

* Fri Sep 26 2014 Remi Collet <rcollet@redhat.com> 5.6.1-0
- test build for upcoming 5.6.1
- use default system cipher list by Fedora policy
  http://fedoraproject.org/wiki/Changes/CryptoPolicy

* Wed Sep 24 2014 Remi Collet <rcollet@redhat.com> 5.6.1-0.2.RC1
- provides nginx configuration (see #1142298)

* Fri Sep 12 2014 Remi Collet <rcollet@redhat.com> 5.6.1-0.1.RC1
- php 5.6.1RC1

* Wed Sep  3 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-1.2
- ensure gd-last 2.1.0-3, with libvpx support, is used

* Fri Aug 29 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-1.1
- enable libvpx on EL 6 (with libvpx 1.3.0)

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-1
- PHP 5.6.0 is GA
- fix ZTS man pages, upstream patch for 67878

* Wed Aug 20 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.22.RC4
- backport rawhide stuff for F21+ and httpd-filesystem
  with support for SetHandler to proxy_fcgi

* Thu Aug 14 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.21.RC4
- php 5.6.0RC4

* Wed Jul 30 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.20.RC3
- php 5.6.0RC3
- fix license handling
- fix zts-php-config --php-binary output #1124605
- cleanup with_libmysql
- add php-litespeed subpackage (/usr/bin/lsphp)

* Fri Jul 25 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.18.RC2
- dont display timezone version in phpinfo (tzdata patch v11)

* Sat Jul 19 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.17.RC2
- test build for #67635

* Mon Jul  7 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.16.RC2
- php 5.6.0RC2

* Mon Jun 23 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.15.RC1
- add workaround for unserialize/mock issue from 5.4/5.5

* Mon Jun 23 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.14.RC1
- fix phpdbg with libedit https://bugs.php.net/67499

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.13.RC1
- php 5.6.0RC1

* Mon Jun 16 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.12.beta4
- test build for serialize

* Tue Jun 10 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.11.beta4
- test build for bug 67410, 67411, 67412, 67413
- fix 67392, dtrace breaks argument unpack

* Thu Jun  5 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.10.beta4
- fix regression introduce in fix for #67118

* Wed Jun  4 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.9.beta4
- php 5.6.0beta4

* Wed May 14 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.8.beta3
- php 5.6.0beta3

* Tue May  6 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.8.201405061030
- new snapshot php5.6-201405061030

* Sat May  3 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.7.beta2
- php 5.6.0beta2

* Thu Apr 10 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.6.beta1
- php 5.6.0beta1

* Wed Apr  9 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.5.201404090430
- new snapshot php5.6-201404090430
- add numerical prefix to extension configuration files
- prevent .user.ini files from being viewed by Web clients
- load php directives only when mod_php is active

* Wed Mar 26 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-0.4.201403261230
- new snapshot php5.6-201403261230
- oci8 version 2.0.9
- opcache version 7.0.4-dev

* Mon Mar 17 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-0.4.201403170630
- new snapshot php5.6-201403170630

* Wed Mar 12 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-0.3.201403120830
- new snapshot php5.6-201403120830
- rebuild against gd-last without libvpx on EL < 7
- oci8 version 2.0.8

* Fri Feb 28 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-0.2.alpha3
- php 5.6.0alpha3
- add php-dbg subpackage
- update php.ini from upstream production template
- move /usr/bin/zts-php to php-cli subpackage

* Wed Feb 26 2014 Remi Collet <rcollet@redhat.com> 5.5.10-0.4.RC1
- php-fpm should own /var/lib/php/session and wsdlcache

* Tue Feb 25 2014 Remi Collet <rcollet@redhat.com> 5.5.10-0.3.RC1
- test build for https://bugs.php.net/66762

* Fri Feb 21 2014 Remi Collet <rcollet@redhat.com> 5.5.10-0.2.RC1
- another test build of 5.5.10RC1
- fix memleak in fileinfo ext
- revert test changes for pcre 8.34

* Thu Feb 20 2014 Remi Collet <rcollet@redhat.com> 5.5.10-0.1.RC1
- test build of 5.5.10RC1

* Tue Feb 18 2014 Remi Collet <rcollet@redhat.com> 5.5.9-2
- upstream patch for https://bugs.php.net/66731

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> 5.5.9-1
- Update to 5.5.9
  http://www.php.net/ChangeLog-5.php#5.5.9
- Install macros to /usr/lib/rpm/macros.d where available.
- Add configtest option to php-fpm ini script (EL)

* Thu Jan 23 2014 Remi Collet <rcollet@redhat.com> 5.5.9-0.1.RC1
- test build of 5.5.9RC1

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 5.5.8-2
- fix _httpd_mmn expansion in absence of httpd-devel

* Mon Jan 20 2014 Remi Collet <rcollet@redhat.com> 5.5.8-2
- test build for https://bugs.php.net/66412

* Wed Jan  8 2014 Remi Collet <rcollet@redhat.com> 5.5.8-1
- update to 5.5.8
- drop conflicts with other opcode caches as both can
  be used only for user data cache

* Wed Jan  8 2014 Remi Collet <rcollet@redhat.com> 5.5.8-0.2.RC1
- another test build of 5.5.8RC1

* Sat Dec 28 2013 Remi Collet <rcollet@redhat.com> 5.5.8-0.1.RC1
- test build of 5.5.8RC1

* Fri Dec 20 2013 Remi Collet <rcollet@redhat.com> 5.5.7-1.1
- test build for https://bugs.php.net/66331

* Wed Dec 11 2013 Remi Collet <rcollet@redhat.com> 5.5.7-1
- update to 5.5.7, fix for CVE-2013-6420
- fix zend_register_functions breaks reflection, php bug 66218
- fix Heap buffer over-read in DateInterval, php bug 66060
- fix fix overflow handling bug in non-x86

* Tue Dec 10 2013 Remi Collet <rcollet@redhat.com> 5.5.7-0.4.RC1
- test build

* Wed Dec 04 2013 Remi Collet <rcollet@redhat.com> 5.5.7-0.3.RC1
- test build

* Mon Dec 02 2013 Remi Collet <rcollet@redhat.com> 5.5.7-0.2.RC1
- test build for https://bugs.php.net/66218
  zend_register_functions breaks reflection

* Thu Nov 28 2013 Remi Collet <rcollet@redhat.com> 5.5.7-0.1.RC1
- test build of 5.5.7RC1

* Wed Nov 13 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-1
- update to 5.5.6

* Tue Nov 12 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.7
- update to 5.5.6, test build

* Fri Nov  8 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.6.RC1
- add --with debug option for debug build

* Wed Nov  6 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.5.RC1
- test buid with opcache changes reverted

* Mon Nov  4 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.4.RC1
- test build opcache with phar build shared
  https://github.com/zendtech/ZendOptimizerPlus/issues/147

* Mon Nov  4 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.3.RC1
- build phar shared, opcache loaded with RTLD_LAZY

* Sat Nov  2 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.2.RC1
- build phar static for opcache dep.

* Sat Nov  2 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.1.RC1
- test build of 5.5.6RC1

* Sun Oct 27 2013 Remi Collet <remi@fedoraproject.org> 5.5.5-2
- rebuild using libicu-last 50.1.2

* Tue Oct 15 2013 Remi Collet <rcollet@redhat.com> - 5.5.5-1
- update to 5.5.5

* Mon Sep 23 2013 Remi Collet <rcollet@redhat.com> - 5.5.4-2
- test build

* Thu Sep 19 2013 Remi Collet <rcollet@redhat.com> - 5.5.4-1
- update to 5.5.4
- improve security, use specific soap.wsdl_cache_dir
  use /var/lib/php/wsdlcache for mod_php and php-fpm
- sync short_tag comments in php.ini with upstream

* Fri Aug 30 2013 Remi Collet <rcollet@redhat.com> - 5.5.4.0.1-201308300430
- test build with -fsanitize=address
- test build for https://bugs.php.net/65564

* Wed Aug 21 2013 Remi Collet <rcollet@redhat.com> - 5.5.3-1
- update to 5.5.3
- build without zip extension, requires php-pecl-zip
- fix typo and add missing entries in php.ini

* Tue Aug 20 2013 Remi Collet <rcollet@redhat.com> - 5.5.3-0
- update to 5.5.3
- test build without zip extension
- fix typo and add missing entries in php.ini

* Mon Aug 19 2013 Remi Collet <rcollet@redhat.com> - 5.5.2-1
- update to 5.5.2

* Thu Aug  8 2013 Remi Collet <remi@fedoraproject.org> - 5.5.2-0.2.RC1
- improve system libzip patch

* Thu Aug  1 2013 Remi Collet <remi@fedoraproject.org> - 5.5.2-0.1.RC1
- 5.5.2RC1

* Fri Jul 26 2013 Remi Collet <remi@fedoraproject.org> - 5.5.1-2
- test build with oracle instantclient 12.1

* Mon Jul 22 2013 Remi Collet <rcollet@redhat.com> - 5.5.1-1
- update to 5.5.1
- add Provides: php(pdo-abi), for consistency with php(api)
  and php(zend-abi)
- improved description for mod_php
- fix opcache ZTS configuration (blacklists in /etc/php-zts.d)
- add missing man pages (phar, php-cgi)
- fix php-enchant summary and description

* Fri Jul 12 2013 Remi Collet <rcollet@redhat.com> - 5.5.0-2
- add security fix for CVE-2013-4113
- add missing ASL 1.0 license
- 32k stack size seems ok for tests on both 32/64bits build

* Mon Jun 24 2013 Remi Collet <rcollet@redhat.com> 5.5.1-0.1.201306240630
- test build (bundled libgd)

* Thu Jun 20 2013 Remi Collet <rcollet@redhat.com> 5.5.0-1
- update to 5.5.0 final

* Fri Jun 14 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.11.RC3
- also drop JSON from sources
- clean conditional for JSON (as removed from the sources)
- clean conditional for FPM (always build)

* Fri Jun 14 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.36.RC3.1
- EL-5 rebuild with gd-last

* Thu Jun 13 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.36.RC3
- drop JSON extension
- build with system GD when 2.1.0 is available

* Thu Jun  6 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.35.RC3
- update to 5.5.0RC3

* Mon May 27 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.34.201305271230.
-test build with systemd gd

* Thu May 23 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.33.RC2
- update to 5.5.0RC2
- add missing options in php-fpm.conf
- improved systemd configuration, documentation about
  /etc/sysconfig/php-fpm being deprecated

* Wed May 22 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.32.201305220430
- test build for https://bugs.php.net/64895

* Sat May 18 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.32.201305181030
- test build with systemd integration (type=notify)

* Wed May  8 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.31.RC1
- update to 5.5.0RC1

* Sat Apr 27 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.30.201305041230
- test build for libgd

* Sat Apr 27 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.29.201304291030
- new snapshot
- review some sub-packages description
- add option to disable json extension

* Thu Apr 25 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.28.beta4
- update to 5.5.0beta4, rebuild with new sources

* Thu Apr 25 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.27.beta4
- update to 5.5.0beta4

* Mon Apr 22 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.27-201304221230
- new snapshot
- try build with system gd 2.1.0

* Thu Apr 18 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.26-201304181030
- new snapshot
- zend_extension doesn't requires full path
- refresh system libzip patch
- drop opcache patch merged upstream

* Thu Apr 11 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.25.beta3
- allow wildcard in opcache.blacklist_filename and provide
  default /etc/php.d/opcache-default.blacklist

* Wed Apr 10 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.24.beta3
- update to 5.5.0beta3

* Thu Apr  4 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.23-201304040630
- new snapshot
- clean old deprecated options

* Thu Mar 28 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.22.beta2
- update to 5.5.0beta2
- Zend Optimizer+ renamed to Zend OPcache
- sync provided configuration with upstream

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.21-201303251230
- new snapshot
- generated parser using system bison, test for https://bugs.php.net/64503

* Wed Mar 20 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.20-201303201430
- new snapshot (beta1)

* Mon Mar 18 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.19-201303180830
- new snapshot
- temporary disable dtrace
- new extension opcache in php-opccache sub-package

* Thu Mar 14 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.18-201303141230
- new snapshot
- hardened build (links with -z now option)
- remove %%config from /etc/rpm/macros.php

* Fri Mar  8 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.17-201303081230
- new snapshot (post alpha 6)
- make php-mysql package optional (and disabled)
- make ZTS build optional (still enabled)

* Thu Feb 28 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.16-201302281430
- new snapshot

* Thu Feb 21 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.16-201302211230
- new snapshot (post alpha 5)

* Wed Feb 13 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.16-201302131030
- enable tokyocabinet and gdbm dba handlers

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.15-201302121230
- new snapshot

* Mon Feb  4 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.14-201302040630
- new snapshot

* Fri Feb  1 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.14-201302010630
- new snapshot

* Mon Jan 28 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.13-201301281030
- new snapshot
- don't display XFAIL tests in report

* Wed Jan 23 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.12-201301230630
- new snapshot, alpha4

* Thu Jan 17 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.11-201301170830
- new snapshot
- fix php.conf to allow MultiViews managed by php scripts

* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.10-201301100830
- new snapshot, alpha3

* Wed Jan  2 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.10-201301021430
- new snapshot

* Mon Dec 24 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.9.201212241030
- new snapshot (post alpha2)
- use xz compressed tarball

* Tue Dec 18 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.9.201212181230
- new snapshot

* Wed Dec 12 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.8.201212121430
- new snapshot

* Tue Dec 11 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.8.201212110630
- patch for unpack

* Tue Dec 11 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.7.201212110630
- prevent php_config.h changes across (otherwise identical) rebuilds
- drop "Configure Command" from phpinfo output

* Tue Dec 11 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.6.201212110630
- new snapshot
- move gmp in new sub-package

* Mon Dec 10 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.6.201212100830
- build sockets, tokenizer extensions shared

* Mon Dec 10 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.5.201212100830
- new snapshot
- enable dtrace

* Tue Dec  4 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.4.201211301534
- build simplexml and xml extensions shared (in php-xml)
- build bz2, calendar, ctype, exif, ftp, gettext and iconv
  extensions shared (in php-common)
- build gmp extension shared (in php-bcmath)
- build shmop extension shared (in php-process)

* Mon Dec  3 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.3.201211301534
- drop some old compatibility provides (php-api, php-zend-abi, php-pecl-*)
- obsoletes php55-*

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.2.201211301534
- update to have zend_execute_ex for xDebug

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.1.201211300857
- Initial work on 5.5.0-dev

* Fri Nov 23 2012 Remi Collet <remi@fedoraproject.org> 5.4.9-2
- add patch for https://bugs.php.net/63588
  duplicated implementation of php_next_utf8_char

* Thu Nov 22 2012 Remi Collet <remi@fedoraproject.org> 5.4.9-1
- update to 5.4.9

* Thu Nov 15 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.5.RC1
- switch back to upstream generated scanner/parser

* Thu Nov 15 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.4.RC1
- use _httpd_contentdir macro and fix php.gif path

* Wed Nov 14 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.3.RC1
- improve system libzip patch to use pkg-config

* Wed Nov 14 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.2.RC1
- use _httpd_moddir macro

* Wed Nov 14 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.1.RC1
- update to 5.4.9RC1
- improves php.conf (use FilesMatch + SetHandler)
- improves filter (httpd module)
- apply ldap_r patch on fedora >= 18 only

* Fri Nov  9 2012 Remi Collet <remi@fedoraproject.org> 5.4.9-0.2.RC1
- sync with rawhide

* Fri Nov  9 2012 Remi Collet <rcollet@redhat.com> 5.4.8-6
- clarify Licenses
- missing provides xmlreader and xmlwriter
- modernize spec

* Thu Nov  8 2012 Remi Collet <remi@fedoraproject.org> 5.4.9-0.1.RC1
- update to 5.4.9RC1
- change php embedded library soname version to 5.4

* Tue Nov  6 2012 Remi Collet <rcollet@redhat.com> 5.4.8-5
- fix _httpd_mmn macro definition

* Mon Nov  5 2012 Remi Collet <rcollet@redhat.com> 5.4.8-4
- fix mysql_sock macro definition

* Thu Oct 25 2012 Remi Collet <rcollet@redhat.com> 5.4.8-3
- fix installed headers

* Tue Oct 23 2012 Joe Orton <jorton@redhat.com> - 5.4.8-2
- use libldap_r for ldap extension

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> 5.4.8-1
- update to 5.4.8
- define both session.save_handler and session.save_path
- fix possible segfault in libxml (#828526)
- php-fpm: create apache user if needed
- use SKIP_ONLINE_TEST during make test
- php-devel requires pcre-devel and php-cli (instead of php)

* Fri Oct  5 2012 Remi Collet <remi@fedoraproject.org> 5.4.8-0.3.RC1
- provides php-phar

* Thu Oct  4 2012 Remi Collet <RPMS@famillecollet.com> 5.4.8-0.2.RC1
- update systzdata patch to v10, timezone are case insensitive

* Thu Oct  4 2012 Remi Collet <RPMS@famillecollet.com> 5.4.8-0.1.RC1
- update to 5.4.8RC1

* Mon Oct  1 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-10
- fix typo in systemd macro

* Mon Oct  1 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-9
- php-fpm: enable PrivateTmp
- php-fpm: new systemd macros (#850268)
- php-fpm: add upstream patch for startup issue (#846858)

* Fri Sep 28 2012 Remi Collet <rcollet@redhat.com> 5.4.7-8
- systemd integration, https://bugs.php.net/63085
- no odbc call during timeout, https://bugs.php.net/63171
- check sqlite3_column_table_name, https://bugs.php.net/63149

* Mon Sep 24 2012 Remi Collet <rcollet@redhat.com> 5.4.7-7
- most failed tests explained (i386, x86_64)

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-6
- fix for http://bugs.php.net/63126 (#783967)

* Wed Sep 19 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-6
- add --daemonize / --nodaemonize options to php-fpm
  upstream RFE: https://bugs.php.net/63085

* Wed Sep 19 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-5
- sync with rawhide
- patch to report libdb version https://bugs.php.net/63117

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-5
- patch to ensure we use latest libdb (not libdb4)

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-4
- really fix rhel tests (use libzip and libdb)

* Tue Sep 18 2012 Remi Collet <rcollet@redhat.com> 5.4.7-3
- fix test to enable zip extension on RHEL-7

* Mon Sep 17 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-2
- remove session.save_path from php.ini
  move it to apache and php-fpm configuration files

* Fri Sep 14 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-1
- update to 5.4.7
  http://www.php.net/releases/5_4_7.php
- php-fpm: don't daemonize

* Thu Sep 13 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-1
- update to 5.4.7

* Mon Sep  3 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-0.2.RC1
- obsoletes php53* and php54*

* Fri Aug 31 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-0.1.RC1
- update to 5.4.7RC1

* Mon Aug 20 2012 Remi Collet <remi@fedoraproject.org> 5.4.6-2
- enable php-fpm on secondary arch (#849490)

* Thu Aug 16 2012 Remi Collet <remi@fedoraproject.org> 5.4.6-1
- update to 5.4.6

* Thu Aug 02 2012 Remi Collet <RPMS@famillecollet.com> 5.4.6-0.1.RC1
- update to 5.4.6RC1

* Fri Jul 20 2012 Remi Collet <RPMS@famillecollet.com> 5.4.5-1
- update to 5.4.5

* Sat Jul 07 2012 Remi Collet <RPMS@famillecollet.com> 5.4.5-0.2.RC1
- update patch for system libzip

* Wed Jul 04 2012 Remi Collet <RPMS@famillecollet.com> 5.4.5-0.1.RC1
- update to 5.4.5RC1 with bundled libzip.

* Mon Jul 02 2012 Remi Collet <RPMS@famillecollet.com> 5.4.4-4
- use system pcre only on fedora >= 14 (version 8.10)
- drop BR for libevent (#835671)
- provide php(language) to allow version check
- define %%{php_version}

* Thu Jun 21 2012 Remi Collet <RPMS@famillecollet.com> 5.4.4-2
- clean spec, sync with rawhide
- add missing provides (core, ereg, filter, standard)

* Wed Jun 13 2012 Remi Collet <Fedora@famillecollet.com> 5.4.4-1
- update to 5.4.4 finale
- fedora >= 15: use /usr/lib/tmpfiles.d instead of /etc/tmpfiles.d
- fedora >= 15: use /run/php-fpm instead of /var/run/php-fpm

* Thu May 31 2012 Remi Collet <Fedora@famillecollet.com> 5.4.4-0.2.RC2
- update to 5.4.4RC2

* Thu May 17 2012 Remi Collet <Fedora@famillecollet.com> 5.4.4-0.1.RC1
- update to 5.4.4RC1

* Wed May 09 2012 Remi Collet <Fedora@famillecollet.com> 5.4.3-1
- update to 5.4.3 (CVE-2012-2311, CVE-2012-2329)

* Thu May 03 2012 Remi Collet <remi@fedoraproject.org> 5.4.2-1
- update to 5.4.2 (CVE-2012-1823)

* Fri Apr 27 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-1
- update to 5.4.1
- use libdb in fedora >= 18 instead of db4

* Fri Apr 13 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-0.3.RC2
- update to 5.4.1RC2

* Sat Mar 31 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-0.2.RC1
- rebuild

* Sat Mar 31 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-0.1.RC1
- update to 5.4.1RC1, split php conf when httpd 2.4

* Tue Mar 27 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-1.1
- sync with rawhide (httpd 2.4 stuff)

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 5.4.0-2
- rebuild against httpd 2.4
- use _httpd_mmn, _httpd_apxs macros
- fix --without-system-tzdata build for Debian et al

* Fri Mar 02 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-1
- update to PHP 5.4.0 finale

* Sat Feb 18 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.16.RC8
- update to 5.4.0RC8

* Sat Feb 04 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.15.RC7
- update to 5.4.0RC7

* Fri Jan 27 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.14.RC6
- build against system libzip (fedora >= 17), patch from spot

* Thu Jan 26 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.13.RC6
- add /etc/sysconfig/php-fpm environment file (#784770)

* Wed Jan 25 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.12.RC6
- keep all ZTS binaries in /usr/bin (with zts prefix)

* Thu Jan 19 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.11.RC6
- update to 5.4.0RC6

* Wed Jan 18 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.10.RC5
- add some fedora patches back (dlopen, easter, phpize)

* Mon Jan 16 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.9.RC5
- improves mysql.sock default path

* Fri Jan 13 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.8.RC5
- update to 5.4.0RC5
- patch for https://bugs.php.net/60748 (mysql.sock hardcoded)
- move session.path from php.ini to httpd/conf.d/php.conf
- provides both ZTS mysql extensions (libmysql/mysqlnd)
- build php cli ZTS binary, in -devel, mainly for test

* Wed Jan 04 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.7.201201041830
- new snapshot (5.4.0RC5-dev) with fix for https://bugs.php.net/60627

* Fri Dec 30 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.6.201112300630
- new snapshot (5.4.0RC5-dev)

* Mon Dec 26 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.6.201112261030
- new snapshot (5.4.0RC5-dev)

* Sat Dec 17 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.5.201112170630
- new snapshot (5.4.0RC4-dev)

* Mon Dec 12 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.4.201112121330
- new snapshot (5.4.0RC4-dev)
- switch to systemd

* Fri Dec 09 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.3.201112091730
- new snapshot (5.4.0RC4-dev)
- removed patch merged upstream for https://bugs.php.net/60392
- clean ini (from upstream production default)

* Sun Nov 13 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.3.201111260730
- new snapshot (5.4.0RC3-dev)
- patch for https://bugs.php.net/60392 (old libicu on EL-5)

* Sun Nov 13 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.3.201111130730
- new snapshot (5.4.0RC2-dev)
- sync with latest changes in 5.3 spec

* Thu Sep 08 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.2.201109081430
- new snapshot
- build mysql/mysqli against both libmysql and mysqlnd (new mysqlnd sub-package)

* Sat Sep 03 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.1.201109031230
- first work on php 5.4
- remove -sqlite subpackage
- move php/modules-zts to php-zts/modules

