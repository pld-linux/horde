# TODO:
# - support for Oracle and Sybase
# - Support SQLite and Oracle in all SQL configurations.
# - LDAP and memcached session handlers.
# - remove config/ (and others in apache.conf) from document root, so
#   apache deny from all not needed.

%define		hordeapp horde
%define		php_min_version 5.2.0
%define		pearname	horde
%include	/usr/lib/rpm/macros.php
Summary:	The common Horde Framework for all Horde modules
Summary(es.UTF-8):	Elementos básicos do Horde Web Application Suite
Summary(pl.UTF-8):	Wspólny szkielet Horde do wszystkich modułów Horde
Summary(pt_BR.UTF-8):	Componentes comuns do Horde usados por todos os módulos
Name:		%{hordeapp}
Version:	4.0.2
Release:	0.6
License:	LGPL
Group:		Applications/WWW
Source0:	http://pear.horde.org/get/horde-%{version}.tgz
# Source0-md5:	937db8f29861a30a68bdeeb2fcd89692
Source1:	%{name}.conf
Source2:	%{name}-lighttpd.conf
Source3:	README.PLD
#Patch0:	%{name}-path.patch
Patch1:		%{name}-shell.disabled.patch
Patch3:		%{name}-blank-admins.patch
Patch4:		%{name}-config-xml.patch
Patch5:		%{name}-mime_drivers.patch
#Patch6:	%{name}-webroot.patch
Patch7:		%{name}-geoip.patch
#Patch8:	%{name}-crypt-detect.patch
URL:		http://www.horde.org/
BuildRequires:	php-channel(pear.horde.org)
BuildRequires:	php-horde-Horde_Role
BuildRequires:	php-pear-PEAR >= 1:1.7.0
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.595
Requires:	php-channel(pear.horde.org)
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-domxml
Requires:	php-filter
Requires:	php-gd
Requires:	php-gettext
Requires:	php-hash
Requires:	php-horde-Horde_Alarm < 2.0.0
Requires:	php-horde-Horde_Argv < 2.0.0
Requires:	php-horde-Horde_Auth < 2.0.0
Requires:	php-horde-Horde_Autoloader < 2.0.0
Requires:	php-horde-Horde_Browser < 2.0.0
Requires:	php-horde-Horde_Core < 2.0.0
Requires:	php-horde-Horde_Date < 2.0.0
Requires:	php-horde-Horde_Exception < 2.0.0
Requires:	php-horde-Horde_Form < 2.0.0
Requires:	php-horde-Horde_Group < 2.0.0
Requires:	php-horde-Horde_Http < 2.0.0
Requires:	php-horde-Horde_Image < 2.0.0
Requires:	php-horde-Horde_LoginTasks < 2.0.0
Requires:	php-horde-Horde_Mime < 2.0.0
Requires:	php-horde-Horde_Nls < 2.0.0
Requires:	php-horde-Horde_Perms < 2.0.0
Requires:	php-horde-Horde_Prefs < 2.0.0
Requires:	php-horde-Horde_Rpc < 2.0.0
Requires:	php-horde-Horde_Serialize < 2.0.0
Requires:	php-horde-Horde_Support < 2.0.0
Requires:	php-horde-Horde_Template < 2.0.0
Requires:	php-horde-Horde_Text_Diff < 2.0.0
Requires:	php-horde-Horde_Text_Filter < 2.0.0
Requires:	php-horde-Horde_Token < 2.0.0
Requires:	php-horde-Horde_Tree < 2.0.0
Requires:	php-horde-Horde_Url < 2.0.0
Requires:	php-horde-Horde_Util < 2.0.0
Requires:	php-horde-Horde_Vfs < 2.0.0
Requires:	php-horde-Horde_View < 2.0.0
Requires:	php-imap
Requires:	php-json
Requires:	php-mbstring
Requires:	php-mcrypt
Requires:	php-pcre
Requires:	php-pear-Log
Requires:	php-pear-Mail
Requires:	php-pear-Mail_Mime
Requires:	php-pear-Net_DNS2
Requires:	php-posix
Requires:	php-session
Requires:	php-xml
Requires:	php-zlib
Requires:	webapps
Requires:	webserver(php) >= 4.1.0
# Suggests: smtpserver(for /usr/lib/sendmail) || smtp server
Suggests:	dpkg
Suggests:	enscript
Suggests:	php-horde-Horde_ActiveSync
Suggests:	php-horde-Horde_DataTree
Suggests:	php-horde-Horde_Db
Suggests:	php-horde-Horde_Feed
Suggests:	php-horde-Horde_Oauth
Suggests:	php-horde-Horde_Service_Facebook
Suggests:	php-horde-Horde_Service_Twitter
Suggests:	php-horde-Horde_SyncMl
Suggests:	php-iconv
Suggests:	php-pear-DB >= 1.7.8
Suggests:	php-pear-Date
Suggests:	php-pear-File
Suggests:	php-pear-HTTP_WebDAV_Server
Suggests:	php-pear-Net_DNS
Suggests:	php-pear-Net_GeoIP
Suggests:	php-pear-SOAP
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

%define		_noautoreq	pear(SOAP.*) pear(Services/Weather.*)

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
%pear_package_setup -d horde_dir=%{_appdir}

mv ./%{php_pear_dir}/data/horde/* .
mv docs/horde/* docs

cp -p %{SOURCE3} .

cd ./%{_appdir}

#%patch0 -p1
%patch1 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1
#%patch6 -p1
%patch7 -p1
#%patch8 -p1 # likely in Horde_Auth package now

rm -f {,*/}.htaccess
for i in config/*.dist; do
	mv $i config/$(basename $i .dist)
done

# Described in documentation as dangerous file...
rm test.php

# remove backup files from patching
find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs,/var/{lib,log}/horde,%{schemadir}}

cd ./%{_appdir}
cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a admin js lib locale rpc services templates themes $RPM_BUILD_ROOT%{_appdir}
#cp -a docs/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
cd -

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

> $RPM_BUILD_ROOT/var/log/horde/%{hordeapp}.log
cp -p scripts/ldap/horde.schema $RPM_BUILD_ROOT%{schemadir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
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

%files
%defattr(644,root,root,755)
%doc README README.PLD scripts
%doc docs/{CHANGES,CODING_STANDARDS,CONTRIBUTING,CREDITS,INSTALL}
%doc docs/{PERFORMANCE,RELEASE,RELEASE_NOTES,SECURITY,TRANSLATIONS,UPGRADING}
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
