# TODO:
# - support for Oracle and Sybase
# - Support SQLite and Oracle in all SQL configurations.
# - LDAP and memcached session handlers.
# - remove config/ (and others in apache.conf) from document root, so
#   apache deny from all not needed.
#
# Conditional build:
%bcond_without	autodeps	# don't BR packages needed only for resolving deps
#
%define		hordeapp horde
#
%include	/usr/lib/rpm/macros.php
Summary:	The common Horde Framework for all Horde modules
Summary(es.UTF-8):	Elementos básicos do Horde Web Application Suite
Summary(pl.UTF-8):	Wspólny szkielet Horde do wszystkich modułów Horde
Summary(pt_BR.UTF-8):	Componentes comuns do Horde usados por todos os módulos
Name:		%{hordeapp}
Version:	3.3.4
Release:	1
License:	LGPL
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/horde/%{hordeapp}-%{version}.tar.gz
# Source0-md5:	4b8f8e73e87ca5f8833515e1c7e4fc64
Source1:	%{name}.conf
Source2:	%{name}-lighttpd.conf
Patch0:		%{name}-path.patch
Patch1:		%{name}-shell.disabled.patch
Patch3:		%{name}-blank-admins.patch
Patch4:		%{name}-config-xml.patch
Patch5:		%{name}-mime_drivers.patch
Patch6:		%{name}-webroot.patch
Patch7:		%{name}-geoip.patch
URL:		http://www.horde.org/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.304
%if %{with autodeps}
BuildRequires:	php-pear-Crypt_Rc4
BuildRequires:	php-pear-Date
BuildRequires:	php-pear-DB
BuildRequires:	php-pear-File
BuildRequires:	php-pear-File_Fstab
BuildRequires:	php-pear-HTTP_Request
BuildRequires:	php-pear-HTTP_WebDAV_Server
BuildRequires:	php-pear-Log
BuildRequires:	php-pear-Mail
BuildRequires:	php-pear-Mail_Mime
BuildRequires:	php-pear-Mail_mimeDecode
BuildRequires:	php-pear-MDB2
BuildRequires:	php-pear-MDB2_Schema
BuildRequires:	php-pear-Net_IMAP
BuildRequires:	php-pear-Net_SMPP_Client
BuildRequires:	php-pear-PEAR
BuildRequires:	php-pear-Services_Weather
BuildRequires:	php-pear-SOAP
BuildRequires:	php-pear-Text_CAPTCHA
BuildRequires:	php-pear-Text_Figlet
BuildRequires:	php-pear-VFS
BuildRequires:	php-pear-XML_SVG
%endif
Requires(triggerpostun):	grep
Requires(triggerpostun):	sed >= 4.0
Requires:	php-pear-Log
Requires:	php-pear-Mail
Requires:	php-pear-Mail_Mime
Requires:	php(domxml)
Requires:	php(gd)
Requires:	php(gettext)
Requires:	php(imap)
Requires:	php(json)
Requires:	php(mbstring)
Requires:	php(mcrypt)
Requires:	php(pcre)
Requires:	php(posix)
Requires:	php(session)
Requires:	php(xml)
Requires:	php(zlib)
Requires:	webserver(php) >= 4.1.0
Requires:	webapps
# Suggests: smtpserver(for /usr/lib/sendmail) || smtp server
Suggests:	dpkg
Suggests:	enscript
Suggests:	php-pear-Date
Suggests:	php-pear-DB >= 1.7.8
Suggests:	php-pear-File
Suggests:	php-pear-HTTP_WebDAV_Server
Suggests:	php-pear-Net_GeoIP
Suggests:	php-pear-Services_Weather
Suggests:	php-pecl-fileinfo
Suggests:	php-pecl-geoip
Suggests:	php-pecl-lzf
Suggests:	php-pecl-memcache
Suggests:	php-pecl-pam
Suggests:	php-pecl-radius
Suggests:	php-pecl-sasl
Suggests:	php-pecl-ssh2
Suggests:	php-pecl-uuid
Suggests:	php-pecl-xdiff
Suggests:	samba-client
Suggests:	source-highlight
Suggests:	wv
Suggests:	xlhtml
Obsoletes:	horde-mysql
Obsoletes:	horde-pgsql
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'pear(Horde.*)' 'pear(XML/WBXML.*)' 'pear(SyncML.*)' 'pear(Text/.*)' 'pear(Net/IMSP.*)' 'pear(XML/sql2xml.php)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}
%define		_webapps	/etc/webapps
%define		_webapp		%{hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		schemadir	/usr/share/openldap/schema

%description
The Horde Framework provides a common structure and interface for
Horde modules (such as IMP, a web-based mail program). This RPM is
required for all other Horde module RPMS.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Horde and its modules) please visit <http://www.horde.org/>.

%description -l pl.UTF-8
Szkielet Horde dostarcza wspólną strukturę oraz interfejs dla modułów
Horde, takich jak IMP (obsługa poczty poprzez WWW). Ten pakiet jest
wymagany dla wszystkich innych modułów Horde.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Więcej informacji (włącznie z pomocą dla Horde
i jego modułów) można znaleźć na stronie <http://www.horde.org/>.

%description -l pt_BR.UTF-8
Este pacote provê uma interface e estrutura comuns para os módulos
Horde (como IMP, um programa de webmail) e é requerido por todos os
outros módulos Horde.

O Projeto Horde é constituído por diversos aplicativos web escritos em
PHP, todos liberados sob a GPL. Para mais informações (incluindo ajuda
com relação ao Horde e seus módulos), por favor visite
<http://www.horde.org/>.

%package -n openldap-schema-horde
Summary:	Horde LDAP schema
Summary(pl.UTF-8):	Schemat LDAP dla Horde
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-schema-rfc2739
Requires:	openldap-servers
Requires:	sed >= 4.0

%description -n openldap-schema-horde
This package contains horde.schema for openldap.

%description -n openldap-schema-horde -l pl.UTF-8
Ten pakiet zawiera horde.schema dla pakietu openldap.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

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
cp -a admin js lib locale rpc services templates themes $RPM_BUILD_ROOT%{_appdir}
cp -a docs/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

> $RPM_BUILD_ROOT/var/log/horde/%{hordeapp}.log
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
%openldap_schema_register %{schemadir}/horde.schema -d core
%service -q ldap restart

%postun -n openldap-schema-horde
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/horde.schema
	%service -q ldap restart
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
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
	if [ -f /etc/horde.org/%{hordeapp}/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/$i{,.rpmnew}
		mv -f /etc/horde.org/%{hordeapp}/$i.rpmsave %{_sysconfdir}/$i
	fi
done

if [ -f /etc/horde.org/apache-%{hordeapp}.conf.rpmsave ]; then
	mv -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	cp -f /etc/horde.org/apache-%{hordeapp}.conf.rpmsave %{_sysconfdir}/apache.conf
	cp -f /etc/horde.org/apache-%{hordeapp}.conf.rpmsave %{_sysconfdir}/httpd.conf
	rm -f /etc/horde.org/apache-%{hordeapp}.conf.rpmsave
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
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/conf.xml
%dir %{_sysconfdir}/registry.d
%{_sysconfdir}/registry.d/README

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/admin
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/js
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/rpc
%{_appdir}/services
%{_appdir}/templates
%{_appdir}/themes

%dir %attr(770,root,http) /var/log/horde
%dir %attr(770,root,http) /var/lib/horde
%attr(770,root,http) %ghost /var/log/horde/%{hordeapp}.log

%files -n openldap-schema-horde
%defattr(644,root,root,755)
%{schemadir}/*.schema
