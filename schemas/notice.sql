create table notice (
day Date DEFAULT toDate(ts),
ts DateTime,
uid String,
orig_h String,
orig_p String,
resp_h String,
resp_p String,
fuid String,
file_mime_type String,
file_desc String,
proto Enum8(''=0, 'udp'=1, 'tcp'=2, 'icmp'=3),
-- Note could be enum, but would require keeing it up to date
note String,
msg String,
sub String,
src String,
dst String,
p String,
n UInt64,
peer_descr String,
actions Array(String),
suppress_for UInt32,
dropped Enum8('F'=0, 'T'=1)
)
ENGINE = MergeTree(day,sipHash64(uid), (day,sipHash64(uid), uid), 8192);
