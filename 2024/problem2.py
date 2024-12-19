reports = []

for line in open("input2.txt").readlines():
    reports.append([int(n) for n in line.strip().split(" ")])


def is_valid_report(report):
    prev = report[0]
    asc = None
    for n in report[1:]:
        diff = n - prev
        if diff == 0:
            return False

        if abs(diff) < 1 or abs(diff) > 3:
            return False

        if asc is None:
            asc = diff > 0
        elif asc and diff < 0:
            return False
        elif not asc and diff > 0:
            return False

        prev = n
    return True


def is_valid_report_lax(report):
    if is_valid_report(report):
        return True

    for i in range(len(report)):
        if is_valid_report(report[:i] + report[i + 1:]):
            return True

    return False


print(sum(is_valid_report(r) for r in reports))
print(sum(is_valid_report_lax(r) for r in reports))