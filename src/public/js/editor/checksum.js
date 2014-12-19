/* Feel free to move this function, I couldn't figure out the best place to put
 * it. It requires the two libraries, adler32.js and canonical-json.js */

function checksum(object) {
  /* canonicalJson returns JSON in a known order with no spaces. The escaping
   * and URI functions are the most compatible hack to convert the string to
   * UTF-8. Sum is part of the adler32 library. 1 is a magic number shared with
   * the Python (it's actually default in both but I don't want to rely on it
   * staying that way). */
  return sum(unescape(encodeURIComponent(canonicalJson(object))), 1);
}
