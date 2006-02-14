# TODO:
# - support for Oracle and Sybase
# - Support SQLite and Oracle in all SQL configurations.
# - LDAP and memcached session handlers.
# - remove config/ (and others in apache.conf) from document root, so
#   apache deny from all not needed.
# - put docs/CREDITS to package, rather in doc (so installations with
#   --excludedocs have functional horde?)
# - patch prefs.xml to include default path to GeoIP /usr/share/GeoIP/GeoIP.dat
#
# Conditional build:
%bcond_without	autodeps	# don't BR packages needed only for resolving deps
#
%define	_hordeapp horde
#define	_snap	2006-01-15
%define	_rc		rc3
%define	_rel	0.1
#
%include	/usr/lib/rpm/macros.php
Summary:	The common Horde Framework for all Horde modules
Summary(es):	Elementos b�sicos do Horde Web Application Suite
Summary(pl):	Wsp�lny szkielet Horde do wszystkich modu��w Horde
Summary(pt_BR):	Componentes comuns do Horde usados por todos os m�dulos
Name:		%{_hordeapp}
Version:	3.1
Release:	%{?_rc:1.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	LGPL
Group:		Applications/WWW
#Source0:	ftp://ftp.horde.org/pub/horde/%{_hordeapp}-%{version}.tar.gz
#Source0:	ftp://ftp.horde.org/pub/snaps/%{_snap}/%{_hordeapp}-FRAMEWORK_3-%{_snap}.tar.gz
Source0:	ftp://ftp.horde.org/pub/horde/%{_hordeapp}-%{version}-%{_rc}.tar.gz
# Source0-md5:	ed640e7118a20a66ea6667c494a98fd5
Source1:	%{name}.conf
Source2:	%{name}-lighttpd.conf
Patch0:		%{name}-path.patch
Patch1:		%{name}-shell.disabled.patch
Patch2:		%{name}-util-h3.patch
Patch3:		%{name}-blank-admins.patch
Patch4:		%{name}-config-xml.patch
Patch100:	%{name}-branch.diff
URL:		http://www.horde.org/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	tar >= 1:1.15.1
%if %{with autodeps}
BuildRequires:	php-pear-Crypt_Rc4
BuildRequires:	php-pear-DB
BuildRequires:	php-pear-Date
BuildRequires:	php-pear-File
BuildRequires:	php-pear-HTTP_Request
BuildRequires:	php-pear-HTTP_WebDAV_Server
BuildRequires:	php-pear-Log
BuildRequires:	php-pear-Mail
BuildRequires:	php-pear-Mail_Mime
BuildRequires:	php-pear-Net_IMAP
BuildRequires:	php-pear-PEAR
BuildRequires:	php-pear-SOAP
BuildRequires:	php-pear-Services_Weather
BuildRequires:	php-pear-VFS
BuildRequires:	php-pear-XML_SVG
%endif
Requires(triggerpostun):	grep
Requires(triggerpostun):	sed >= 4.0
Requires:	apache(mod_access)
Requires:	apache(mod_alias)
Requires:	apache(mod_dir) >= 1.3.22
Requires:	php >= 3:4.1.0
Requires:	php-domxml
Requires:	php-gettext >= 3:4.1.0
Requires:	php-imap >= 3:4.1.0
Requires:	php-mcrypt >= 3:4.1.0
Requires:	php-pcre >= 3:4.1.0
Requires:	php-posix >= 3:4.1.0
Requires:	php-session >= 3:4.1.0
Requires:	php-xml >= 3:4.1.0
Requires:	php-zlib >= 3:4.1.0
# Requires: php-pear-{Log,Mail,Mail_Mime
# Requires: php-pear-DB >= 1.6.0 if database_used
# Requires: php-pear-File if import csv wanted
# Requires: php-pear-Date if import calendar data is accessed
# Requires: php-pear-Services_Weather if weather.com service block is used in portal.
# Suggests: php-pecl-fileinfo || (deprecated)php-mime_magic
# Suggests: php-pecl-memcache if memcached SessionHandler is used
# Suggests: smtpserver(for /usr/lib/sendmail) || smtp server
Requires:	webapps
Requires:	webserver = apache
Obsoletes:	horde-mysql
Obsoletes:	horde-pgsql
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(XML/WBXML.*)' 'pear(Horde.*)' 'pear(SyncML.*)' 'pear(Text/.*)' 'pear(Net/IMSP.*)' 'pear(XML/sql2xml.php)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}
%define		_webapps	/etc/webapps
%define		_webapp		%{_hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		schemadir	/usr/share/openldap/schema

%description
The Horde Framework provides a common structure and interface for
Horde modules (such as IMP, a web-based mail program). This RPM is
required for all other Horde module RPMS.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Horde and its modules) please visit <http://www.horde.org/>.

%description -l pl
Szkielet Horde dostarcza wsp�ln� struktur� oraz interfejs dla modu��w
Horde, takich jak IMP (obs�uga poczty poprzez WWW). Ten pakiet jest
wymagany dla wszystkich innych modu��w Horde.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Wi�cej informacji (w��cznie z pomoc� dla Horde
i jego modu��w) mo�na znale�� na stronie <http://www.horde.org/>.

%description -l pt_BR
Este pacote prov� uma interface e estrutura comuns para os m�dulos
Horde (como IMP, um programa de webmail) e � requerido por todos os
outros m�dulos Horde.

O Projeto Horde � constitu�do por diversos aplicativos web escritos em
PHP, todos liberados sob a GPL. Para mais informa��es (incluindo ajuda
com rela��o ao Horde e seus m�dulos), por favor visite
<http://www.horde.org/>.

%package -n openldap-schema-horde
Summary:	Horde LDAP schema
Summary(pl):	Schemat LDAP dla Horde
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers
Requires:	sed >= 4.0

%description -n openldap-schema-horde
This package contains horde.schema for openldap.

%description -n openldap-schema-horde -l pl
Ten pakiet zawiera horde.schema dla pakietu openldap.

%prep
%setup -qcT -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1
#%patch100 -p1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1

rm -f {,*/}.htaccess
for i in config/*.dist; do
	mv $i config/$(basename $i .dist)
done

# Described in documentation as dangerous file...
rm test.php

# remove backup files from patching
find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

# enable if you want to update patch0
%if 0
sed -i -e "
s#dirname(__FILE__) . '/..#'%{hordedir}#g
" config/registry.php.dist
exit 1
%endif

cat > README.PLD << 'EOF'
IMPORTANT:
Default horde installation will auto authorize You as Administrator, but due to
security concerns the Administrator is not granted Administrator privileges.
If You want to add Yourself to admins list (to administer Horde via web
interface), please change %{_sysconfdir}/conf.php:
$conf['auth']['admins'] = array('Administrator');

Depending on authorization You choose, You need to create Horde database tables.
Look into directory %{_docdir}/%{name}-%{version}/scripts/sql
to find out how to do this for Your database.

If You've chosen LDAP authorization, please install php-ldap package.
To configure your openldap server to use horde schema, install
openldap-schema-horde package.

NOTE: You don't need SQL database for Authorization if You use LDAP for authorization.

If you want to use MaxMind GeoIP Hostname Country lookup, install
GeoIP package and go to:

Configuration -> Horde -> Hostname -> Country Lookup and set GeoIP.dat path to: %{_datadir}/GeoIP/GeoIP.dat

EOF
# '

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs,/var/{lib,log}/horde,%{schemadir}}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a admin js services lib locale templates themes $RPM_BUILD_ROOT%{_appdir}

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_defaultdocdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

> $RPM_BUILD_ROOT/var/log/horde/%{_hordeapp}.log
install scripts/ldap/horde.schema $RPM_BUILD_ROOT%{schemadir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<'EOF'
Please read README.PLD from documentation.
EOF

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

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}


%triggerpostun -- horde < 3.0.7-1.4
for i in conf.php hooks.php mime_drivers.php motd.php nls.php prefs.php registry.php; do
	if [ -f /etc/horde.org/%{_hordeapp}/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/$i{,.rpmnew}
		mv -f /etc/horde.org/%{_hordeapp}/$i.rpmsave %{_sysconfdir}/$i
	fi
done

if [ -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave ]; then
	mv -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	cp -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave %{_sysconfdir}/apache.conf
	cp -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave %{_sysconfdir}/httpd.conf
	rm -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave
fi

if [ -L /etc/apache/conf.d/99_horde.conf ]; then
	/usr/sbin/webapp register apache %{_webapp}
	rm -f /etc/apache/conf.d/99_horde.conf
	%service -q apache reload
fi
if [ -L /etc/httpd/httpd.conf/99_horde.conf ]; then
	/usr/sbin/webapp register httpd %{_webapp}
	rm -f /etc/httpd/httpd.conf/99_horde.conf
	%service -q httpd reload
fi

%files
%defattr(644,root,root,755)
%doc README README.PLD scripts util
%doc docs/{CHANGES,CODING_STANDARDS,CONTRIBUTING,CREDITS,HACKING,INSTALL}
%doc docs/{PERFORMANCE,RELEASE_NOTES,SECURITY,TODO,TRANSLATIONS,UPGRADING}
%attr(750,root,http) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/conf.xml

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

%files -n openldap-schema-horde
%defattr(644,root,root,755)
%{schemadir}/*.schema
