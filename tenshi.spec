Summary:	Log parsing and notification program
Summary(pl.UTF-8):	Program do analizy logów i powiadamiania
Name:		tenshi
Version:	0.15
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dev.inversepath.com/tenshi/%{name}-%{version}.tar.gz
# Source0-md5:	3eb858893e29f0f6e7fb9f58f653a5b1
Source1:	%{name}.init
Source2:	%{name}.tmpfiles
Patch0:		%{name}-root.patch
Patch1:		%{name}-config.patch
URL:		http://www.inversepath.com/tenshi.html
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun):	rc-scripts
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Obsoletes:	wasabi
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/tenshi

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

%description -l pl.UTF-8
Tenshi to program do monitorowania logów zaprojektowany do oglądania
jednego lub większej liczby plików logów pod kątem linii pasujących do
zdefiniowanych przez użytkownika wyrażeń regularnych i raportowania
tych dopasowań. Wyrażenia regularne są przypisywane do kolejek
mających częstotliwość alarmowania i listę adresatów pocztowych.

Kolejki mogą być konfigurowane do wysyłania powiadomień zaraz po
napotkaniu linii w logu lub wysyłania regularnych raportów.

Dodatkowo nieciekawe pola z linii logów (takie jak numery procesów)
mogą być pokrywane standardowymi operatorami grupowania wyrażeń
regularnych ( ). Daje to bardziej przejrzyste i bardziej czytelne
raporty. Wszystkie raporty są oddzielane nazwą hosta, a wszystkie
wiadomości są tak skondensowane, jak to tylko możliwe.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man8,/var/run/tenshi} \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

%{__rm} -r  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 175 %{name}
%useradd -u 175 -d %{_sysconfdir} -g %{name} -c "Tenshi User" %{name}

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc CREDITS Changelog README tenshi.conf
%attr(755,root,root) %{_sbindir}/*
%attr(750,root,tenshi) %dir %{_sysconfdir}
%attr(640,root,tenshi) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man8/*
%dir %attr(775,root,tenshi) /var/run/tenshi
/usr/lib/tmpfiles.d/%{name}.conf
