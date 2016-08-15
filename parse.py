#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import time
import hashlib
from random import shuffle

answer_dict = {}


def usage(argv):
    print "USAGE:"
    print "\t %s --gen-subject <data-file> <answer-file> <times>" % (argv[0])
    print "\t %s --gen-answer <data-file> <answer-file>" % (argv[0])
    print "\t %s --score <data-file> <answer-file>" % (argv[0])


class Subject(object):
    def __init__(self, title):
        self.title = title
        self.body = []
        self.hash = hashlib.md5(title).hexdigest().upper()
        self.answer = None
        self.idx = None
        self.allidx = None

    def append(self, choice):
        self.body.append(choice)

    def output_answer(self, f):
        f.write("%d %s %s %s\n" % (self.idx, self.hash, self.answer, self.title))

    def output(self, f):
        f.write(self.title)
        f.write("\r\n")
        for b in self.body:
            f.write("    %s" % (b))
            f.write("\r\n")

        f.write("\r\n")
        f.write("\r\n")


def gen_filename():
    prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return prefix


def parse_title(title):
    if title.find("（苏联）") >= 0:
        title = title.replace("（苏联）", "<苏联>")

    title = title.replace("(", "（")
    title = title.replace(")", "）")

    pos1 = title.find("（")
    pos2 = title.find("）")

    title = title[:pos1 + 3] + title[pos2:]
    return title


def parse_line(line, collect):
    l = line.strip()
    l.replace("\r", "")
    l.replace("\n", "")
    if (len(l) == 0):
        return

    last_subject = None
    if (len(collect) > 0):
        last_subject = collect[-1]

    c = l[0]
    if c.isdigit():
        idx = l.find(".") + 1
        while(l[idx] == " " or l[idx] == "\t"):
            l = l[:idx] + l[idx + 1:]

        l = parse_title(l)
        subject = Subject(l)
        collect.append(subject)
    elif c.isalpha():
        if (last_subject is not None):
            if c.lower() == "a" and l[1] == ".":
                while(l[2] == " " or l[2] == "\t"):
                    l = l[:2] + l[3:]

            last_subject.append(l)


class CorrectAnswer(object):
    def __init__(self, idx, val):
        self.idx = idx
        self.val = val


def load_correct_answer(file):
    global answer_dict
    with open(file, "r") as fp:
        for line in fp:
            line = line.strip()
            if len(line) > 5:
                data = line.split(" ")
                answer_dict[data[1]] = CorrectAnswer(data[0], data[2])


def parse_correct_answer(file):
    global answer_dict
    with open(file, "r") as fp:
        for line in fp:
            line = line.strip()
            if len(line) < 2:
                continue
            data = line.split(" ")
            answer_dict[data[0]] = data[1].upper()


def gen_subject(argv):
    collect = []
    with open(argv[2], "r") as fp:
        for line in fp:
            parse_line(line, collect)

    times = int(argv[3])
    for i in range(times):
        fname = gen_filename()
        with open("data/" + fname, "w") as fp:
            shuffle(collect)
            for subject in collect:
                subject.output(fp)
        print fname
        time.sleep(1)


def gen_answer(argv):
    parse_correct_answer(argv[3])

    collect = []
    with open(argv[2], "r") as fp:
        for line in fp:
            parse_line(line, collect)

    idx = 1
    with open("data/" + "anser", "w") as fp:
        for subject in collect:
            subject.answer = answer_dict[str(idx)]
            subject.idx = idx
            subject.output_answer(fp)
            idx += 1


def parse_val(title):
    if title.find("（苏联）") >= 0:
        title = title.replace("（苏联）", "<苏联>")

    title = title.replace("(", "（")
    title = title.replace(")", "）")
    pos1 = title.find("（")
    pos2 = title.find("）")

    val = title[pos1 + 3:pos2]
    return val.strip()


class Answer(object):
    def __init__(self, title):
        self.title = parse_title(title)
        self.hash = hashlib.md5(self.title).hexdigest().upper()
        self.val = parse_val(title)

    def fire(self):
        global answer_dict
        if self.hash not in answer_dict:
            print "found error hash %s on title: %s" % (self.hash, self.title)
            return

        correct_answer = answer_dict[self.hash]

        if correct_answer.val != self.val:
            print "Error %s -> %s \t title: %s " % (self.val, correct_answer.val, self.title)


def load_answer(file):
    answers = []
    with open(file, "r") as fp:
        for line in fp:
            line = line.strip()
            offset = line.find(".")
            if offset > 0:
                idx = line[:offset]
                if idx.isdigit():
                    a = Answer(line)
                    answers.append(a)
    return answers


def do_score(argv):
    dfile = argv[2]
    afile = argv[3]
    answers = load_answer(dfile)
    load_correct_answer(afile)

    for a in answers:
        a.fire()


if __name__ == '__main__':
    argv = sys.argv
    if (len(argv) < 3):
        usage(argv)
        exit(1)

    if argv[1] == "--gen-subject":
        gen_subject(argv)
    elif argv[1] == "--gen-answer":
        gen_answer(argv)
    elif argv[1] == "--score":
        do_score(argv)
    else:
        usage(argv)
        exit(1)

