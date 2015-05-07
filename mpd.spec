#####################
# Hardcode PLF build
%define build_plf 1
#####################

%{?_with_plf: %{expand: %%global build_plf 1}}

%if %{build_plf}
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif

Summary:	The Music Player Daemon
Name:		mpd
Version:	0.17.2
Release:	3
License:	GPLv2+
Group:		Sound
Url:		http://mpd.wikia.com/
Source0:	http://downloads.sourceforge.net/musicpd/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}.init
Source3:	%{name}.logrotate
Source4:	README.urpmi
Source5:	%{name}.service

BuildRequires:	avahi-common-devel
BuildRequires:	libatomic_ops-devel
BuildRequires:	libmikmod-devel
BuildRequires:	libmpcdec-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(ao)
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(flac++)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(shout)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(vorbis)
%if %{build_plf}
BuildRequires:	faad2-devel
%endif
Requires(pre,post,preun,postun):	rpm-helper

%description
Music Player Daemon (MPD) allows remote access for playing music (MP3, Ogg
Vorbis, FLAC, Mod, and wave files) and managing playlists. MPD is designed
for integrating a computer into a stereo system that provides control for music
playback over a local network. It is also makes a great desktop music player,
especially if your a console junkie, like frontend options, or restart X often.

%if %{build_plf}
This package is in restricted repository because it is built with AAC support
of libfaad2, which is patent-protected.
%endif

%prep
%setup -q

%build
%configure2_5x \
	--with-alsa-prefix=%{_prefix} \
	--enable-ao \
	--enable-curl \
%if ! %{build_plf}
	--disable-aac \
%endif
	--enable-sqlite
%make

%install
%makeinstall_std

mkdir -p %{buildroot}/var/lib/mpd
touch %{buildroot}/%{_localstatedir}/lib/mpd/mpd.db
touch %{buildroot}/%{_localstatedir}/lib/mpd/mpdstate
mkdir -p %{buildroot}/var/log/mpd
touch %{buildroot}/var/log/mpd/mpd.log
touch %{buildroot}/var/log/mpd/mpd.error
mkdir -p %{buildroot}/var/run/mpd
mkdir -p %{buildroot}/%{_localstatedir}/lib/mpd/playlists
mkdir -p %{buildroot}/%{_localstatedir}/lib/mpd/music
mkdir -p %{buildroot}/lib/systemd/system

install -D %{SOURCE1} %{buildroot}/etc/mpd.conf
install -D %{SOURCE2} %{buildroot}/%{_initrddir}/%{name}
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install %{SOURCE4} doc/README.urpmi
rm -rf %{buildroot}/%{_docdir}/mpd

install -D %{SOURCE5} %{buildroot}/lib/systemd/system/

%pre
%_pre_useradd %{name} %{_localstatedir}/lib/%{name} /bin/false
usermod -g audio %{name}

%post
if [ $1 -eq 1 ]
then
%create_ghostfile %{_localstatedir}/lib/mpd/mpd.db mpd audio 644
%create_ghostfile %{_localstatedir}/lib/mpd/mpdstate mpd audio 644
%create_ghostfile /var/log/mpd/mpd.log mpd audio 644
%create_ghostfile /var/log/mpd/mpd.error mpd audio 644
fi
#echo If you want to run mpd as a service, please read
#echo /usr/share/doc/mpd-%{version}/README.MDK
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%doc README UPGRADING AUTHORS NEWS doc/mpdconf.example doc/*.urpmi
%{_bindir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man5/*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,mpd,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_initrddir}/%{name}
%defattr(644,mpd,audio)
%attr(755,mpd,audio) %dir %{_localstatedir}/lib/mpd
%attr(755,mpd,audio) %dir %{_localstatedir}/lib/mpd/music
%attr(755,mpd,audio) %dir %{_localstatedir}/lib/mpd/playlists
%ghost %{_localstatedir}/lib/mpd/mpd.db
%ghost %{_localstatedir}/lib/mpd/mpdstate
%attr(755,mpd,audio) %dir /var/log/mpd
%attr(755,mpd,audio) %dir /var/run/mpd
%ghost /var/log/mpd/mpd.log
%ghost /var/log/mpd/mpd.error
%attr(644,root,root) /lib/systemd/system/%{name}.service

