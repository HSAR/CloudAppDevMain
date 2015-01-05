/* Adapted from Mirko Kiefer's node module canonical-json
 * (https://github.com/mirkokiefer/canonical-json) */
/* Lines with comments have been modified from the original. */

var isObject = function(a) {
  return Object.prototype.toString.call(a) === '[object Object]'; /* add ; */
}; /* add ; */

var copyObjectWithSortedKeys = function(object) {
  if (isObject(object)) {
    var newObj = {}; /* add ; */
    var keysSorted = Object.keys(object).sort(); /* add ; */
    var key; /* add ; */
    for (var i = 0, len = keysSorted.length; i < len; i++) {
      key = keysSorted[i]; /* add ; */
      newObj[key] = copyObjectWithSortedKeys(object[key]); /* add ; */
    }
    return newObj; /* add ; */
  } else if (Array.isArray(object)) {
    return object.map(copyObjectWithSortedKeys); /* add ; */
  } else {
    return object; /* add ; */
  }
}; /* add ; */

function canonicalJson(object) { /* convert from node module to generic JS */
  return JSON.stringify(copyObjectWithSortedKeys(object)); /* add ; */
}
