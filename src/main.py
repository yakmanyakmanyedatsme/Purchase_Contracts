import reports
import sys
import pickle as pck


def main(*arglist):
    print("run main operation")
    files = []
    for arg in arglist:
        files.append(arglist)
    repObject = reports(files)
    reportList = repObject.apply_all_documents()
    tri_grams = open("tri_grams.pck")
    pck.dump(reportList, tri_grams)


if __name__ == '__main__':
    sys.exit(main())
