#!/usr/bin/env python3

from math import sqrt
import numpy as np
import sys


class DescStats:
    def __init__(self, batch_size=1):
        self.batch_size = batch_size
        self.data = []
        self.weights = []
        self.means = []
        self.vardevs = []
        self.medians = []

    def outfmt(self, alist):
        alist = list(map(lambda x: round(x, 3), alist))
        return map(str, alist)

    def run(self):
        # Reading incoming numbers
        for incline in sys.stdin:
            incline = incline.rstrip()

            # Time to exit
            # Any accumulated data not in a batch
            # is discarded
            if incline == "QQ":
                break

            # Convert to a float
            incnum = None
            try:
                incnum = float(incline)
                self.data.append(incnum)
            except:
                print("Skipping - not a number", file=sys.stderr)
                continue

            # Calculate and output
            if len(self.data) % self.batch_size == 0:
                ########## Mean
                # Find the mean and count of incoming data
                self.means.append(np.mean(self.data))
                self.weights.append(len(self.data))

                # Find the weighted average of the means
                mmeans = np.average(self.means, weights=self.weights)

                ########## Std dev
                # Std dev we treat a little different
                if self.batch_size == 1:
                    # If batch size of one, run for all of the means
                    # Which are really individual samples
                    mstddevs = np.std(self.means)
                else:
                    # Find the variances of incoming data
                    self.vardevs.append(np.var(self.data))

                    # Find the weighted average of the variances and get the sq root (stddev)
                    mstddevs = sqrt(np.average(self.vardevs, weights=self.weights))

                ########## Median
                # Concatenate current medians with incoming
                cmbmedians = np.concatenate((self.data, self.medians))

                # Determine the local median and keep it
                self.medians.append(np.median(self.data))

                # Find the median of medians
                mmedians = np.median(cmbmedians)

                ########## Output
                # Output and clear data list
                res = [mmeans, mstddevs, mmedians]
                print(",".join(self.outfmt(res)))
                self.data = []


def get_batch_size(batchsz):
    # Grab batch size
    default_batchsz = 1

    # If the argument is not empty, try to make it an integer
    if batchsz == "":
        print(
            "Number of batches must be a number - setting default value for batches - "
            + str(default_batchsz)
        )
        return default_batchsz

    else:
        try:
            batchsz = int(batchsz)
        except:
            print(
                "Number of batches must be a number - setting default value for batches - "
                + str(default_batchsz)
            )
            return default_batchsz

    # Check if less than zero
    if batchsz <= 0:
        print(
            "Number of batches cannot less than or equal to 0 - Setting default value for batches - "
            + str(default_batchsz)
        )
        return default_batchsz

    return batchsz


if __name__ == "__main__":
    batch_size = ""
    if len(sys.argv) > 1:
        batch_size = sys.argv[1]

    # Instantiate and run
    ds = DescStats(get_batch_size(batch_size))
    ds.run()
