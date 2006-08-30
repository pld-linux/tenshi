%include	/usr/lib/rpm/macros.perl
Summary:	Log parsing and notification program
Summary(pl):	Program do analizy log�w i powiadamiania
Name:		tenshi
Version:	0.5.1
Release:	1
License:	ISC
Group:		Applications/System
Source0:	http://dev.gentoo.org/~lcars/tenshi/%{name}-%{version}.tar.gz
# Source0-md5:	44361d5d8defc5170146f467a8825413
Source1:	%{name}.init
Patch0:		%{name}-root.patch
URL:		http://www.gentoo.org/proj/en/infrastructure/tenshi/index.xml
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	rpm-perlprov
Requires(post,preun):	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Obsoletes:	wasabi
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tenshi is a log monitoring program, designed to watch one or more log
files for lines matching user defined regular expressions and report
on the matches. The regular expressions are assigned to queues which
have an alert interval and a list of mail recipients.

Queues can be set to send a notification as soon as there is a log
line assigned to it, or to send periodic reports.

Additionally, uninteresting fields in the log lines (such as PID
numbers) can be masked with the standard regular expression grouping
operators ( ). This allows cleaner and more readable reports. All
reports are separated by hostname and all messages are condensed when
possible.

%description -l pl
Tenshi to program do monitorowania log�w zaprojektowany do ogl�dania
jednego lub wi�kszej liczby plik�w log�w pod k�tem linii pasuj�cych do
zdefiniowanych przez u�ytkownika wyra�e� regularnych i raportowania
tych dopasowa�. Wyra�enia regularne s� przypisywane do kolejek
maj�cych cz�stotliwo�� alarmowania i list� adresat�w pocztowych.

Kolejki mog� by� konfigurowane do wysy�ania powiadomie� zaraz po
napotkaniu linii w logu lub wysy�ania regularnych raport�w.

Dodatkowo nieciekawe pola z linii log�w (takie jak numery proces�w)
mog� by� pokrywane standardowymi operatorami grupowania wyra�e�
regularnych ( ). Daje to bardziej przejrzyste i bardziej czytelne
raporty. Wszystkie raporty s� oddzielane nazw� hosta, a wszystkie
wiadomo�ci s� tak skondensowane, jak to tylko mo�liwe.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man8,/etc/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc CREDITS Changelog README
%attr(755,root,root) %{_sbindir}/*
%attr(750,root,root) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man8/*
