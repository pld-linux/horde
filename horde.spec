# TODO:
# - support for Oracle and Sybase

%define		_relcand	RC3

Summary:	The common Horde Framework for all Horde modules
Summary(es):	Elementos b�sicos do Horde Web Application Suite
Summary(pl):	Wsp�lny szkielet Horde do wszystkich modu��w Horde
Summary(pt_BR):	Componentes comuns do Horde usados por todos os m�dulos
Name:		horde
Version:	2.1
Release:	%{_relcand}.0.1
License:	LGPL
Vendor:		The Horde Project
Group:		Development/Languages/PHP
Source0:	ftp://ftp.horde.org/pub/horde/tarballs/%{name}-%{version}-%{_relcand}.tar.gz
Source1:	%{name}.conf
URL:		http://www.horde.org/
PreReq:		apache-mod_dir >= 1.3.22
Prereq:		perl
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
BuildArch:	noarch
Obsoletes:	horde-mysql
Obsoletes:	horde-pgsql
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apachedir	/etc/httpd
%define		apachegroup	http
%define		contentdir	/home/httpd

%description
The Horde Framework provides a common structure and interface for
Horde modules (such as IMP, a web-based mail program). This RPM is
required for all other Horde module RPMS.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Horde and its modules) please visit http://www.horde.org/.

%description -l pl
Szkielet Horde dostarcza wsp�ln� struktur� oraz interfejs dla modu��w
Horde, takich jak IMP (obs�uga poczty poprzez www). Ten pakiet jest
wymagany dla wszystkich innych modu��w Horde.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je�eli chcesz si� dowiedzie� czego� wi�cej (tak�e help
do IMP'a) zajrzyj na stron� http://www.horde.org

%description -l pt_BR
Este pacote prov� uma interface e estrutura comuns para os m�dulos Horde
(como IMP, um programa de webmail) e � requerido por todos os outros
m�dulos Horde.

O Projeto Horde � constitu�do por diversos aplicativos web escritos em PHP,
todos liberados sob a GPL. Para mais informa��es (incluindo ajuda com
rela��o ao Horde e seus m�dulos), por favor visite http://www.horde.org/.

%prep
%setup -q

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

gzip -9nf README docs/HACKING docs/CONTRIBUTING docs/CODING_STANDARDS docs/CHANGES

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
%doc *.gz docs/*.gz scripts/db/*
%dir %{contentdir}/html/horde
%{contentdir}/html/horde/*.php
%{contentdir}/html/horde/admin
%{contentdir}/html/horde/graphics
%{contentdir}/html/horde/lib
%{contentdir}/html/horde/locale
%{contentdir}/html/horde/templates
%{apachedir}/horde
%attr(640,root,http) %config(noreplace) %{apachedir}/horde.conf
%attr(750,root,http) %dir %{contentdir}/html/horde/config
%attr(640,root,http) %{contentdir}/html/horde/config/*.dist
%attr(640,root,http) %config %{contentdir}/html/horde/config/*.php
%attr(640,root,http) %config(noreplace) %{contentdir}/html/horde/config/.htaccess
