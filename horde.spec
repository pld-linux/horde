# TODO:
# - support for Oracle and Sybase
#
%include	/usr/lib/rpm/macros.php
Summary:	The common Horde Framework for all Horde modules
Summary(es):	Elementos básicos do Horde Web Application Suite
Summary(pl):	Wspólny szkielet Horde do wszystkich modu³ów Horde
Summary(pt_BR):	Componentes comuns do Horde usados por todos os módulos
Name:		horde
Version:	2.2.3
Release:	1
License:	LGPL
Vendor:		The Horde Project
Group:		Development/Languages/PHP
Source0:	ftp://ftp.horde.org/pub/horde/tarballs/%{name}-%{version}.tar.gz
# Source0-md5:	27e5c190a6a22a6aa2201e6b714a653d
Source1:	%{name}.conf
Patch0:		%{name}-XML_xml2sql.patch
URL:		http://www.horde.org/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
PreReq:		apache-mod_dir >= 1.3.22
Requires(post):	grep
Requires(post,preun):	perl
Requires:	apache >= 1.3.22
Requires:	php >= 4.1.0
Requires:	php-gettext >= 4.1.0
Requires:	php-imap >= 4.1.0
Requires:	php-mcrypt >= 4.1.0
Requires:	php-pear >= 4.1.0
Requires:	php-pcre >= 4.1.0
Requires:	php-posix >= 4.1.0
Requires:	php-session >= 4.1.0
Requires:	php-xml >= 4.1.0
Obsoletes:	horde-mysql
Obsoletes:	horde-pgsql
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apachedir	/etc/httpd
%define		contentdir	/home/services/httpd
%define		htmldir		%{contentdir}/html

%description
The Horde Framework provides a common structure and interface for
Horde modules (such as IMP, a web-based mail program). This RPM is
required for all other Horde module RPMS.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Horde and its modules) please visit http://www.horde.org/.

%description -l pl
Szkielet Horde dostarcza wspóln± strukturê oraz interfejs dla modu³ów
Horde, takich jak IMP (obs³uga poczty poprzez www). Ten pakiet jest
wymagany dla wszystkich innych modu³ów Horde.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je¿eli chcesz siê dowiedzieæ czego¶ wiêcej (tak¿e help
do IMP'a) zajrzyj na stronê http://www.horde.org

%description -l pt_BR
Este pacote provê uma interface e estrutura comuns para os módulos Horde
(como IMP, um programa de webmail) e é requerido por todos os outros
módulos Horde.

O Projeto Horde é constituído por diversos aplicativos web escritos em PHP,
todos liberados sob a GPL. Para mais informações (incluindo ajuda com
relação ao Horde e seus módulos), por favor visite http://www.horde.org/.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{apachedir} \
	$RPM_BUILD_ROOT%{contentdir}/html/horde/{admin,config,graphics,lib,locale,templates,util}

ln -fs %{contentdir}/html/horde/config $RPM_BUILD_ROOT%{apachedir}/horde 
install	%{SOURCE1}	$RPM_BUILD_ROOT%{apachedir}/
cp -pR	*.php		$RPM_BUILD_ROOT%{contentdir}/html/horde

for i in config graphics lib locale templates util; do
	cp -pR $i/*	$RPM_BUILD_ROOT%{contentdir}/html/horde/$i
done
for i in config lib locale templates; do
	cp -p $i/.htaccess	$RPM_BUILD_ROOT%{contentdir}/html/horde/$i
done

# Described in documentation as dangerous file...
rm $RPM_BUILD_ROOT%{contentdir}/html/horde/test.php

# bit unclean..
cd $RPM_BUILD_ROOT%{contentdir}/html/horde/config
for i in *.dist; do cp $i `basename $i .dist`; done

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "Changing apache configuration"
perl -pi -e 's/$/ index.php/ if (/DirectoryIndex\s.*index\.html/ && !/index\.php/);' %{apachedir}/httpd.conf
grep -i 'Include.*horde.conf$' %{apachedir}/httpd.conf >/dev/null 2>&1
if [ $? -eq 0 ]; then
	perl -pi -e 's/^#+// if (/Include.*horde.conf$/i);' %{apachedir}/httpd.conf
else
	echo "Include %{apachedir}/horde.conf" >>%{apachedir}/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start http daemon."
fi

cat <<_EOF2_
IMPORTANT:
If you are installing for the first time, you must now
create the Horde database tables. Look into directory 
/usr/share/doc/%{name}-%{version}/scripts/db
to find out how to do this for your database.
_EOF2_

%postun
if [ $1 -eq 0 ]; then
	echo "Changing apache configuration"
	perl -pi -e 's/^/#/ if (/^Include.*horde.conf$/i);' %{apachedir}/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	else
		echo "Run \"/etc/rc.d/init.d/httpd start\" to start http daemon."
	fi
fi

%files
%defattr(644,root,root,755)
%doc README docs/{HACKING,CONTRIBUTING,CODING_STANDARDS,CHANGES}
%dir %{htmldir}/horde
%{htmldir}/horde/*.php
%{htmldir}/horde/admin
%{htmldir}/horde/graphics
%{htmldir}/horde/lib
%{htmldir}/horde/locale
%{htmldir}/horde/templates
%{htmldir}/horde/util
%{apachedir}/horde
%attr(640,root,http) %config(noreplace) %{apachedir}/horde.conf
%attr(750,root,http) %dir %{htmldir}/horde/config
%attr(640,root,http) %{htmldir}/horde/config/*.dist
%attr(640,root,http) %config(noreplace) %{htmldir}/horde/config/*.php
%attr(640,root,http) %config(noreplace) %{contentdir}/html/horde/config/.htaccess
