import linsrc from "./search/linsrc.py?raw";
import binsrc from "./search/binsrc.py?raw";

import bubble from "./sort/bubble.py?raw";
import insertion from "./sort/insertion.py?raw";
import merge from "./sort/merge.py?raw";
import quick from "./sort/quick.py?raw";
import selection from "./sort/selection.py?raw";

import type { PageId, Filename, Pages } from "$lib";

export const defaultCode: Pages = {
  search: {
    "linsrc.py": { content: linsrc, version: 1 },
    "binsrc.py": { content: binsrc, version: 1 },
  },
  sort: {
    "bubble.py": { content: bubble, version: 1 },
    "insertion.py": { content: insertion, version: 1 },
    "merge.py": { content: merge, version: 1 },
    "quick.py": { content: quick, version: 1 },
    "selection.py": { content: selection, version: 1 },
  }
};
