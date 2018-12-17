#!/usr/bin/perl

use strict;
BEGIN {
  push @INC, '../lib' if -f '../lib/Lingua/BO/Wylie.pm';
  push @INC, './lib' if -f './lib/Lingua/BO/Wylie.pm';
  push @INC, '/srv/www/perl-lib' if -f '/srv/www/perl-lib/Lingua/BO/Wylie.pm';
}

use utf8;
use Lingua::BO::Wylie;
use Getopt::Long;

my $text = utf8::unicode_to_native(@ARGV[0]);

my $wl = new Lingua::BO::Wylie();
my $truc = $wl->to_wylie($text);
print $truc;
