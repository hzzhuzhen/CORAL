package com.freeal.commons.utils;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.function.Function;

public class JwtUtil {
    // 秘钥明文
    private static final String SECRET = "CORAL";
    // 有效时间8个小时
    private static final long EXPIRATION_TIME = TimeUnit.HOURS.toMillis(8);

    // 生成token
    public static String generateToken(String username) {
        Map<String, Object> claims = new HashMap<>();
        return createToken(claims, username);
    }

    private static String createToken(Map<String, Object> claims, String subject) {
        return Jwts.builder()
                .setClaims(claims)
                .setSubject(subject)
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
                .signWith(SignatureAlgorithm.HS256, SECRET)
                .compact();
    }

    // 从token中提取用户名
    public static String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    // 从token中提取指定的claim
    public static <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    private static Claims extractAllClaims(String token) {
        return Jwts.parser()
                .setSigningKey(SECRET)
                .parseClaimsJws(token)
                .getBody();
    }

    // 验证token是否过期
    public static Boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }

    private static Date extractExpiration(String token) {
        return extractClaim(token, Claims::getExpiration);
    }

    // 验证token
    public static Boolean validateToken(String token, String username) {
        final String extractedUsername = extractUsername(token);
        return (extractedUsername.equals(username) && !isTokenExpired(token));
    }

    public static void main(String[] args) {
        String token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzIyOTMwNDQ2LCJpYXQiOjE3MjI5MjY4NDZ9.-RbSqd1_G-Fk-Do4c_3VhqCdZ32aGvyIWME6zEl6N5Y";
        //System.out.println(generateToken("1"));
        System.out.println(validateToken(token, "3"));
        //System.out.println(extractUsername(token));
    }
}
