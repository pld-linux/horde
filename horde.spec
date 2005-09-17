%define	_hordeapp horde
#define	_snap	2005-08-01
#define	_rc		rc1
%define	_rel	2

# TODO:
# - support for Oracle and Sybase
# - Support SQLite and Oracle in all SQL configurations.
# - LDAP and memcached session handlers.
# - remove config/ (and others in apache.conf) from document root, so
#   apache deny from all not needed.
# - put docs/CREDITS to package, rather in doc (so installations with
#   --excludedocs have functional horde?)
#
%include	/usr/lib/rpm/macros.php
Summary:	The common Horde Framework for all Horde modules
Summary(es):	Elementos básicos do Horde Web Application Suite
Summary(pl):	Wspólny szkielet Horde do wszystkich modu³ów Horde
Summary(pt_BR):	Componentes comuns do Horde usados por todos os módulos
Name:		%{_hordeapp}
Version:	3.0.5
Release:	%{?_rc:0.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	LGPL
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/horde/%{_hordeapp}-%{version}.tar.gz
# Source0-md5:	31ee0819be4efe44819f8ffef5db5365
Source1:	%{name}.conf
Source2:	http://www.maxmind.com/download/geoip/database/GeoIP.dat.gz
# Source2-md5:	4f29410e385065eaa37037c1b1a44695
Patch0:		%{name}-path.patch
Patch1:		%{name}-shell.disabled.patch
Patch2:		%{name}-util-h3.patch
Patch3:		%{name}-blank-admins.patch
Patch4:		%{name}-config-xml.patch
URL:		http://www.horde.org/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.226
BuildRequires:	tar >= 1:1.15.1
Requires(triggerpostun):	grep
Requires(triggerpostun):	sed >= 4.0
Requires:	apache >= 1.3.33-3
Requires:	apache(mod_access)
Requires:	apache(mod_alias)
Requires:	apache(mod_dir) >= 1.3.22
Requires:	php >= 3:4.1.0
Requires:	php-domxml
Requires:	php-gettext >= 3:4.1.0
Requires:	php-imap >= 3:4.1.0
Requires:	php-mcrypt >= 3:4.1.0
Requires:	php-pcre >= 3:4.1.0
Requires:	php-pear-Log
Requires:	php-pear-PEAR
Requires:	php-posix >= 3:4.1.0
Requires:	php-session >= 3:4.1.0
Requires:	php-xml >= 3:4.1.0
Requires:	php-zlib >= 3:4.1.0
Obsoletes:	horde-mysql
Obsoletes:	horde-pgsql
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(XML/WBXML.*)' 'pear(Horde.*)' 'pear(Text/.*)' 'pear(Net/IMSP.*)'

%define		hordedir	/usr/share/horde
%define		_sysconfdir	/etc/horde.org
%define		_appdir		%{hordedir}
%define		schemadir	/usr/share/openldap/schema

%description
The Horde Framework provides a common structure and interface for
Horde modules (such as IMP, a web-based mail program). This RPM is
required for all other Horde module RPMS.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Horde and its modules) please visit <http://www.horde.org/>.

%description -l pl
Szkielet Horde dostarcza wspóln± strukturê oraz interfejs dla modu³ów
Horde, takich jak IMP (obs³uga poczty poprzez WWW). Ten pakiet jest
wymagany dla wszystkich innych modu³ów Horde.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je¿eli chcesz siê dowiedzieæ czego¶ wiêcej (tak¿e help
do IMP-a) zajrzyj na stronê <http://www.horde.org/>.

%description -l pt_BR
Este pacote provê uma interface e estrutura comuns para os módulos
Horde (como IMP, um programa de webmail) e é requerido por todos os
outros módulos Horde.

O Projeto Horde é constituído por diversos aplicativos web escritos em
PHP, todos liberados sob a GPL. Para mais informações (incluindo ajuda
com relação ao Horde e seus módulos), por favor visite
<http://www.horde.org/>.

%package -n openldap-schema-horde
Summary:	Horde LDAP schema
Summary(pl):	Schemat LDAP dla Horde
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	sed >= 4.0
Requires:	openldap-servers

%description -n openldap-schema-horde
This package contains horde.schema for openldap.

%description -n openldap-schema-horde -l pl
Ten pakiet zawiera horde.schema dla pakietu openldap.

%prep
%setup -q -c -T -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1

sed -i -e "
s#dirname(__FILE__) . '/..#'%{hordedir}#g
" config/registry.php.dist

# Described in documentation as dangerous file...
rm test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp} \
	$RPM_BUILD_ROOT%{_appdir}/{admin,js,services} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes} \
	$RPM_BUILD_ROOT/var/{lib,log}/horde \
	$RPM_BUILD_ROOT%{schemadir}

cp -a *.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.php.dist; do
	cp -a $i $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/$(basename $i .dist)
done
cp -p config/conf.xml	$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.xml
touch					$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php.bak

cp -pR  admin/*                 $RPM_BUILD_ROOT%{_appdir}/admin
cp -pR  js/*                    $RPM_BUILD_ROOT%{_appdir}/js
cp -pR  services/*              $RPM_BUILD_ROOT%{_appdir}/services

cp -pR  lib/*                   $RPM_BUILD_ROOT%{_appdir}/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{_appdir}/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{_appdir}/templates
cp -pR  themes/*                $RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{_hordeapp} $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_defaultdocdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} 		$RPM_BUILD_ROOT%{_sysconfdir}/apache-%{_hordeapp}.conf

# MaxMind GeoIP Hostname Country lookup
install %{SOURCE2}		$RPM_BUILD_ROOT/var/lib/horde/

> $RPM_BUILD_ROOT/var/log/horde/%{_hordeapp}.log

install scripts/ldap/horde.schema $RPM_BUILD_ROOT%{schemadir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{_hordeapp}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{_hordeapp}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<'EOF'

IMPORTANT:
Default horde installation will auto authorize You as Administrator, but due
security concerns the Administrator is not granted Administrator privileges.
If You want to add Yourself to admins list (to administer Horde via web
interface), please change %{_sysconfdir}/%{_hordeapp}/conf.php:
$conf['auth']['admins'] = array('Administrator');

Depending on authorization You choose, You need to create Horde database tables.
Look into directory %{_docdir}/%{name}-%{version}/scripts/sql
to find out how to do this for Your database.

If You've chosen LDAP authorization, please install php-ldap package.
To configure your openldap server to use horde schema, install
openldap-schema-horde package.

NOTE: You don't need SQL database for Auhtorization if You use LDAP for authorization.

If you want to use MaxMind GeoIP Hostname Country lookup do 'gunzip /var/lib/horde/GeoIP.dat.gz'
and enable this function in horde configuration.

EOF
# '

fi

%post -n openldap-schema-horde
if ! grep -q %{schemadir}/horde.schema /etc/openldap/slapd.conf; then
	sed -i -e '
		/^include.*local.schema/{
			i\
include		%{schemadir}/horde.schema
		}
		# enable dependant schemas: core.schema
		/^#include.*\(core\)\.schema/{
			s/^#//
		}
	' /etc/openldap/slapd.conf
fi

if [ -f /var/lock/subsys/ldap ]; then
    /etc/rc.d/init.d/ldap restart >&2
fi

%postun -n openldap-schema-horde
if [ "$1" = "0" ]; then
	if grep -q %{schemadir}/horde.schema /etc/openldap/slapd.conf; then
		sed -i -e '
		/^include.*\/usr\/share\/openldap\/schema\/horde.schema/d

		# for symmetry it would be nice if we disable enabled schemas in post,
		# but we really can not do that, it would break something else.
		' /etc/openldap/slapd.conf
	fi

	if [ -f /var/lock/subsys/ldap ]; then
		/etc/rc.d/init.d/ldap restart >&2 || :
	fi
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%triggerpostun -- horde <= 2.2.7-2
for i in horde.php html.php lang.php mime_drivers.php mime_mapping.php motd.php prefs.php registry.php; do
	if [ -f /home/services/httpd/html/horde/config/$i.rpmsave ]; then
		cp -f %{_sysconfdir}/%{_hordeapp}/$i %{_sysconfdir}/%{_hordeapp}/$i.rpmnew
		mv -f /home/services/httpd/html/horde/config/$i.rpmsave %{_sysconfdir}/%{_hordeapp}/$i
	fi
done

%triggerpostun -- horde <= 3.0.3-2.23
# apache1 confdir
if [ -f /etc/apache/apache.conf ]; then
	if grep -q '^Include conf\.d/\*\.conf' /etc/apache/apache.conf; then
		sed -i -e '
			/^Include.*horde\.conf/d
		' /etc/apache/apache.conf
	else
		# they're still using old apache.conf
		sed -i -e '
			s,^Include.*horde\.conf,Include conf.d/*_horde.conf,
		' /etc/apache/apache.conf
	fi
fi

if [ -f /etc/apache/horde.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache-%{_hordeapp}.conf{,.rpmnew}
	mv -f /etc/apache/horde.conf.rpmsave %{_sysconfdir}/apache-%{_hordeapp}.conf
fi

if [ -f /etc/httpd/horde.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache-%{_hordeapp}.conf{,.rpmnew}
	mv -f /etc/httpd/horde.conf.rpmsave %{_sysconfdir}/apache-%{_hordeapp}.conf
fi

# unified location
if [ -f %{_sysconfdir}/apache.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache-%{_hordeapp}.conf{,.rpmnew}
	mv -f %{_sysconfdir}/apache.conf.rpmsave %{_sysconfdir}/apache-%{_hordeapp}.conf
fi

if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache reload 1>&2
fi

if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd reload 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README scripts util
%doc docs/{CHANGES,CODING_STANDARDS,CONTRIBUTING,CREDITS,HACKING,INSTALL}
%doc docs/{PERFORMANCE,RELEASE_NOTES,SECURITY,TODO,TRANSLATIONS,UPGRADING}
%dir %{_sysconfdir}
%attr(750,root,http) %dir %{_sysconfdir}/%{_hordeapp}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{_hordeapp}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{_hordeapp}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{_hordeapp}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/admin
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/js
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/services
%{_appdir}/templates
%{_appdir}/themes

%dir %attr(770,root,http) /var/log/horde
%dir %attr(770,root,http) /var/lib/horde
%ghost %attr(770,root,http) /var/log/horde/%{_hordeapp}.log
%attr(640,root,http) /var/lib/horde/GeoIP.dat.gz

%files -n openldap-schema-horde
%defattr(644,root,root,755)
%{schemadir}/*.schema
