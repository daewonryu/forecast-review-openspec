# TypeScript/JavaScript Coding Style Guide

A comprehensive, framework-agnostic coding style guide for TypeScript and JavaScript development.

---

## Table of Contents

1. [Overview and Interaction Guidelines](#1-overview-and-interaction-guidelines)
2. [Code Quality Standards](#2-code-quality-standards)
3. [TypeScript Conventions](#3-typescript-conventions)
4. [Function Guidelines](#4-function-guidelines)
5. [Low-Level Syntax Rules](#5-low-level-syntax-rules)
6. [API Communication Conventions](#6-api-communication-conventions)
7. [Testing Guidelines](#7-testing-guidelines)
8. [File Structure and Modules](#8-file-structure-and-modules)
9. [Documentation](#9-documentation)
10. [Code Generation Checklist](#10-code-generation-checklist)

---

## 1. Overview and Interaction Guidelines

### 1.1 Purpose

This guide establishes consistent coding standards for TypeScript and JavaScript projects. It ensures that all team members—from junior to senior developers—produce clean, maintainable, and uniform code.

### 1.2 How to Use This Guide

1. **Read thoroughly** before starting development on the project.
2. **Bookmark the checklist** (Section 10) for quick reference during code reviews.
3. **Configure your IDE** to match the styling rules (Prettier, ESLint).
4. **When in doubt**, refer to the specific section or ask a team member.

### 1.3 Core Principles

- **Readability over cleverness**: Code is read more often than it is written.
- **Consistency over preference**: Team conventions take precedence over personal style.
- **Explicitness over implicitness**: Make intentions clear through naming and types.
- **Simplicity over complexity**: Choose the simplest solution that solves the problem.

---

## 2. Code Quality Standards

### 2.1 Naming Conventions

#### Variables (General)

Use `camelCase` for all variable declarations. Avoid abbreviations and ensure names are descriptive.

```typescript
// Good: camelCase, descriptive names
const userAccountBalance = 1000
const isAuthenticated = true
const selectedProductId = 'prod-123'
const hasPermission = false

// Bad: abbreviations, unclear names
const usrAccBal = 1000
const auth = true
const selProdId = 'prod-123'
const perm = false
```

#### Constants (Read-only)

Use `SCREAMING_SNAKE_CASE` for constants that are truly immutable and represent configuration or fixed values.

```typescript
// Good: SCREAMING_SNAKE_CASE for constants
const MAX_RETRY_COUNT = 3
const API_BASE_URL = 'https://api.example.com'
const DEFAULT_PAGE_SIZE = 30
const MILLISECONDS_PER_SECOND = 1000

// Bad: camelCase for constants
const maxRetryCount = 3
const apiBaseUrl = 'https://api.example.com'
```

#### Arrays

Suffix array variables with `List` to clearly indicate they hold multiple items.

```typescript
// Good: suffix with 'List'
const userList: User[] = []
const transactionList: Transaction[] = []
const errorMessageList: string[] = []

// Bad: no clear indication of array
const users: User[] = []
const transactions: Transaction[] = []
```

#### Option Arrays (Select, Checkbox, Radio)

For arrays used in form controls (Selectbox, Checkbox, RadioButton), use `SCREAMING_SNAKE_CASE` with `_OPTION_LIST` suffix. Option objects must follow the `{ label, value }` standard.

```typescript
// Good: SCREAMING_SNAKE_CASE + _OPTION_LIST for form options
const GENDER_OPTION_LIST: Option<string>[] = [
  { label: 'Male', value: 'M' },
  { label: 'Female', value: 'F' },
  { label: 'Other', value: 'O' },
]

const RECORD_STATUS_OPTION_LIST: Option<RecordStatus>[] = [
  { label: 'All', value: RecordStatus.ALL },
  { label: 'Active', value: RecordStatus.ACTIVE },
  { label: 'Inactive', value: RecordStatus.INACTIVE },
]

const PAGE_SIZE_OPTION_LIST: Option<number>[] = [
  { label: '30 items', value: 30 },
  { label: '50 items', value: 50 },
  { label: '100 items', value: 100 },
]

// Variables receiving values from these options
const selectGenderValue = 'M'
const checkboxStatusValue = RecordStatus.ACTIVE
const radioSizeValue = 30
```

#### Objects

Declare objects separately by concern. Use descriptive names that indicate the object's purpose.

```typescript
// Good: separate objects by concern
const tableOptions = {
  pageSize: 30,
  sortField: 'createdAt',
  sortOrder: 'desc',
}

const filterOptions = {
  status: RecordStatus.ACTIVE,
  dateRange: { start: '2024-01-01', end: '2024-12-31' },
}

// Bad: mixed concerns in single object
const options = {
  pageSize: 30,
  status: RecordStatus.ACTIVE,
  sortField: 'createdAt',
}
```

#### Event Handlers

Follow the pattern: `handle` + `Event` + `Subject`

```typescript
// Good: handle + Event + Subject pattern
const handleClickSubmitButton = () => { /* ... */ }
const handleChangeEmailInput = (e: ChangeEvent<HTMLInputElement>) => { /* ... */ }
const handleCloseModal = () => { /* ... */ }
const handleSelectCategory = (categoryId: string) => { /* ... */ }
const handleSubmitForm = (data: FormData) => { /* ... */ }

// Bad: inconsistent naming
const submitButtonClick = () => { /* ... */ }
const onEmailChange = () => { /* ... */ }
const closeModalHandler = () => { /* ... */ }
```

### 2.2 Styling Rules

| Rule | Standard |
|------|----------|
| Line length | 100 characters or fewer |
| Indentation | 2 spaces |
| Semicolons | Omit (configurable per project) |
| Quotes | Single quotes for strings |
| Trailing commas | Use in multiline structures |
| Blank lines | One blank line between logical sections |

```typescript
// Good: follows styling rules
const calculateTotalPrice = (
  itemList: CartItem[],
  discountRate: number,
): number => {
  const subtotal = itemList.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0,
  )

  const discount = subtotal * (discountRate / 100)
  
  return subtotal - discount
}

// Bad: violates styling rules
const calculateTotalPrice = (itemList: CartItem[], discountRate: number): number => {
    const subtotal = itemList.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const discount = subtotal * (discountRate / 100);
    return subtotal - discount;
}
```

---

## 3. TypeScript Conventions

### 3.1 Type Declarations

Use `PascalCase` for all type and interface names.

```typescript
// Good: PascalCase for types and interfaces
interface UserProfile {
  userId: string
  displayName: string
  email: string
  createdAt: Date
}

type RequestStatus = 'pending' | 'success' | 'error'

type UserId = string

interface ApiResponse<T> {
  data: T
  status: number
  message: string
}
```

### 3.2 Type Imports

Always use `import type` for type-only imports. This improves build performance and makes the intent clear.

```typescript
// Good: Use 'import type' for type-only imports
import type { UserProfile, RequestStatus } from '@/types/user'
import type { AxiosResponse, AxiosError } from 'axios'

// Regular imports for values
import { validateEmail, formatDate } from '@/utils'

// Mixed imports
import { UserService } from '@/services/user'
import type { UserProfile } from '@/types/user'
```

### 3.3 Interface vs Type

Use `interface` for object shapes that may be extended. Use `type` for unions, primitives, and computed types.

```typescript
// Good: interface for extensible object shapes
interface BaseEntity {
  id: string
  createdAt: Date
  updatedAt: Date
}

interface User extends BaseEntity {
  email: string
  name: string
}

// Good: type for unions and computed types
type Status = 'active' | 'inactive' | 'pending'
type Nullable<T> = T | null
type UserKeys = keyof User
```

### 3.4 Enum Usage

Use `enum` instead of `as const` objects for better type safety and IDE support.

```typescript
// Good: Use enum
enum RecordStatus {
  ALL = 'ALL',
  READY = 'READY',
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  DELETED = 'DELETED',
}

enum HttpMethod {
  GET = 'GET',
  POST = 'POST',
  PUT = 'PUT',
  DELETE = 'DELETE',
}

// Usage
const status: RecordStatus = RecordStatus.ACTIVE
if (status === RecordStatus.ACTIVE) {
  // ...
}

// Bad: as const pattern
const RecordStatus = {
  ALL: 'ALL',
  READY: 'READY',
  ACTIVE: 'ACTIVE',
} as const
```

### 3.5 Namespace for Type Grouping

Use `namespace` to group related types, especially for API-related types. This provides clear organization and avoids naming conflicts.

```typescript
// Good: Group related types using namespace
export namespace User {
  export interface Profile {
    userId: string
    displayName: string
    email: string
  }

  export interface CreateRequestBody {
    email: string
    name: string
    password: string
  }

  export interface UpdateRequestBody {
    name?: string
    email?: string
  }

  export interface SearchRequestParams {
    keyword: string
    page: number
    size: number
  }

  export type ListResponse = Profile[]
}

// Usage
const createUser = async (body: User.CreateRequestBody): Promise<User.Profile> => {
  // ...
}

const searchUsers = async (params: User.SearchRequestParams): Promise<User.ListResponse> => {
  // ...
}
```

### 3.6 Generic Type Naming

Use descriptive names for complex generics. Single letters are acceptable for simple, well-known patterns.

```typescript
// Good: Descriptive generic names for complex types
interface Repository<TEntity, TId> {
  findById(id: TId): Promise<TEntity | null>
  findAll(): Promise<TEntity[]>
  save(entity: TEntity): Promise<TEntity>
  delete(id: TId): Promise<void>
}

interface PaginatedResponse<TItem> {
  items: TItem[]
  page: number
  totalPage: number
  totalCount: number
}

// Acceptable: Single letter for simple, well-known patterns
const identity = <T>(value: T): T => value

const mapArray = <T, U>(arr: T[], fn: (item: T) => U): U[] => arr.map(fn)
```

---

## 4. Function Guidelines

### 4.1 Function Declaration Style

Prefer arrow function expressions over traditional function declarations.

```typescript
// Good: Arrow function expressions
const calculateTotal = (price: number, quantity: number): number => {
  return price * quantity
}

// Good: Arrow syntax for simple one-liners
const double = (n: number): number => n * 2

const isPositive = (n: number): boolean => n > 0

const formatCurrency = (amount: number): string => `$${amount.toFixed(2)}`

// Bad: Traditional function declarations
function calculateTotal(price: number, quantity: number): number {
  return price * quantity
}

function double(n: number): number {
  return n * 2
}
```

### 4.2 Parameter Limits

Limit functions to a maximum of 2 parameters. When more parameters are needed, use an object with an interface.

```typescript
// Good: Maximum 2 parameters
const createUser = (name: string, email: string) => {
  // ...
}

const calculateDiscount = (price: number, rate: number): number => {
  return price * (1 - rate / 100)
}

// Good: Use interface for 3+ parameters
interface CreateOrderParams {
  userId: string
  productId: string
  quantity: number
  couponCode?: string
  shippingAddress: Address
}

const createOrder = (params: CreateOrderParams) => {
  const { userId, productId, quantity, couponCode, shippingAddress } = params
  // ...
}

// Good: Two parameters where second is an options object
interface FetchOptions {
  page?: number
  size?: number
  sort?: string
}

const fetchUsers = (keyword: string, options: FetchOptions = {}) => {
  // ...
}

// Bad: More than 2 parameters without interface
const createOrder = (
  userId: string,
  productId: string,
  quantity: number,
  couponCode?: string,
) => {
  // ...
}
```

### 4.3 Single Responsibility Principle

Each function should have a single, well-defined responsibility.

```typescript
// Good: Each function does one thing
const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const sendVerificationEmail = async (email: string): Promise<void> => {
  await emailService.send({
    to: email,
    template: 'verification',
  })
}

const logUserAction = (userId: string, action: string): void => {
  logger.info(`User ${userId} performed action: ${action}`)
}

// Bad: Function doing multiple things
const validateAndSendEmail = async (email: string) => {
  // Validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email)) {
    throw new Error('Invalid email')
  }
  
  // Sending
  await emailService.send({ to: email, template: 'verification' })
  
  // Logging
  logger.info(`Verification email sent to ${email}`)
  
  // Navigation (side effect)
  router.push('/email-sent')
}
```

### 4.4 Return Type Annotations

Always explicitly declare return types for functions.

```typescript
// Good: Explicit return types
const add = (a: number, b: number): number => a + b

const getUserById = async (id: string): Promise<User | null> => {
  // ...
}

const processItems = (items: Item[]): ProcessedItem[] => {
  return items.map(item => ({ ...item, processed: true }))
}

// Bad: Implicit return types
const add = (a: number, b: number) => a + b

const getUserById = async (id: string) => {
  // Return type is inferred but not explicit
}
```

---

## 5. Low-Level Syntax Rules

### 5.1 Nullish Coalescing vs Logical OR

Use `??` (nullish coalescing) for null/undefined checks. Use `||` only when you intentionally want to handle all falsy values.

Reference: [MDN - Nullish coalescing operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing_operator)

```typescript
// Good: Use ?? for null/undefined checks
const displayName = user.name ?? 'Anonymous'
const count = data.count ?? 0
const isEnabled = config.enabled ?? true

// Bad: || treats 0, '', false as falsy (potential bugs)
const count = data.count || 10      // Bug: 0 becomes 10
const name = user.name || 'Unknown'  // Bug: '' becomes 'Unknown'
const enabled = config.enabled || true  // Bug: false becomes true

// Good: Use defaultTo from lodash-es for Number types
import { defaultTo } from 'lodash-es'

const quantity = defaultTo(item.quantity, 1)  // Handles NaN as well
const price = defaultTo(product.price, 0)

// When || is appropriate (intentionally handling all falsy values)
const displayValue = inputValue || 'No value provided'  // Empty string should show default
```

### 5.2 Optional Chaining

Use `?.` for safe property access on potentially null/undefined values.

Reference: [MDN - Optional chaining](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining)

```typescript
// Good: Use ?. for safe property access
const street = user?.address?.street
const zipCode = user?.address?.zipCode ?? 'N/A'

// Good: Optional chaining with method calls
const result = callback?.()
const length = data?.items?.length ?? 0

// Good: Optional chaining with array access
const firstItem = items?.[0]
const lastItem = items?.[items.length - 1]

// Bad: Manual null checks (verbose and error-prone)
const street = user && user.address && user.address.street

let length = 0
if (data && data.items) {
  length = data.items.length
}
```

### 5.3 Strict Equality

Always use `===` and `!==` for comparisons. Never use `==` or `!=`.

Reference: [MDN - Strict equality](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Strict_equality)

```typescript
// Good: Always use === and !==
if (status === 'active') {
  // ...
}

if (value !== null) {
  // ...
}

if (count === 0) {
  // ...
}

if (user.role !== UserRole.ADMIN) {
  // ...
}

// Bad: Loose equality (type coercion causes bugs)
if (status == 'active') {
  // ...
}

if (value != null) {  // Also catches undefined unexpectedly
  // ...
}

if (count == 0) {  // '0' == 0 is true
  // ...
}
```

### 5.4 Ternary vs If-Else

Use ternary for simple, single-line conditional assignments. Use if-else for complex logic or multiple statements.

```typescript
// Good: Ternary for simple assignments
const status = isActive ? 'Active' : 'Inactive'
const displayName = user.nickname ?? user.name
const buttonText = isLoading ? 'Loading...' : 'Submit'

// Good: Ternary in template literals
const message = `User is ${isOnline ? 'online' : 'offline'}`

// Good: If-else for complex logic or multiple statements
if (isAdmin) {
  grantAllPermissions()
  logAdminAccess()
  showAdminDashboard()
} else {
  grantBasicPermissions()
  showUserDashboard()
}

// Good: If-else for multiple conditions
if (status === Status.PENDING) {
  showPendingMessage()
} else if (status === Status.APPROVED) {
  showApprovedMessage()
} else if (status === Status.REJECTED) {
  showRejectedMessage()
} else {
  showDefaultMessage()
}

// Bad: Nested ternaries (unreadable)
const result = a ? b ? c : d : e

// Bad: Complex ternary
const value = condition1 
  ? someComplexFunction(param1, param2) 
  : anotherComplexFunction(param3, param4)
```

### 5.5 Early Return Pattern

Use early returns to reduce nesting and improve readability.

```typescript
// Good: Early return to reduce nesting
const processOrder = (order: Order | null): ProcessResult | null => {
  if (!order) {
    return null
  }

  if (order.status === OrderStatus.CANCELLED) {
    return { error: 'Order has been cancelled' }
  }

  if (order.items.length === 0) {
    return { error: 'Order has no items' }
  }

  // Main logic with all preconditions satisfied
  const total = calculateTotal(order.items)
  const tax = calculateTax(total)
  
  return {
    success: true,
    total: total + tax,
  }
}

// Good: Guard clauses at the start
const validateUser = (user: User | null): ValidationResult => {
  if (!user) {
    return { valid: false, error: 'User is required' }
  }

  if (!user.email) {
    return { valid: false, error: 'Email is required' }
  }

  if (!validateEmail(user.email)) {
    return { valid: false, error: 'Invalid email format' }
  }

  return { valid: true }
}

// Bad: Deep nesting
const processOrder = (order: Order | null): ProcessResult | null => {
  if (order) {
    if (order.status !== OrderStatus.CANCELLED) {
      if (order.items.length > 0) {
        const total = calculateTotal(order.items)
        const tax = calculateTax(total)
        return {
          success: true,
          total: total + tax,
        }
      } else {
        return { error: 'Order has no items' }
      }
    } else {
      return { error: 'Order has been cancelled' }
    }
  }
  return null
}
```

### 5.6 Async/Await

Use `async/await` instead of Promise chains for better readability.

Reference: [MDN - async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)

```typescript
// Good: async/await for asynchronous operations
const fetchUserData = async (userId: string): Promise<User> => {
  const response = await fetch(`/api/users/${userId}`)
  
  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.status}`)
  }
  
  const data = await response.json()
  return data
}

// Good: Sequential async operations
const processUserOrder = async (userId: string, orderId: string): Promise<void> => {
  const user = await fetchUser(userId)
  const order = await fetchOrder(orderId)
  const result = await processPayment(user, order)
  await sendConfirmationEmail(user.email, result)
}

// Good: Parallel async operations
const fetchDashboardData = async (): Promise<DashboardData> => {
  const [users, orders, stats] = await Promise.all([
    fetchUsers(),
    fetchOrders(),
    fetchStats(),
  ])
  
  return { users, orders, stats }
}

// Bad: Promise chains (harder to read and debug)
const fetchUserData = (userId: string): Promise<User> => {
  return fetch(`/api/users/${userId}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Failed to fetch user: ${response.status}`)
      }
      return response.json()
    })
    .then(data => data)
}
```

### 5.7 Error Handling

Use `try...finally` when the error is handled elsewhere (e.g., axios interceptor). Use `try...catch` for custom error handling.

```typescript
// Good: try...finally when interceptor handles errors
const fetchData = async (): Promise<void> => {
  setLoading(true)
  try {
    const data = await apiClient.getData()
    setData(data)
  } finally {
    setLoading(false)
  }
}

// Good: try...catch for custom error handling
const submitForm = async (formData: FormData): Promise<Result> => {
  try {
    const result = await apiClient.submit(formData)
    return { success: true, data: result }
  } catch (error) {
    if (error instanceof ValidationError) {
      return { success: false, errors: error.fieldErrors }
    }
    
    if (error instanceof NetworkError) {
      showNotification('Network error. Please try again.')
      return { success: false, errors: ['Network error'] }
    }
    
    // Re-throw unexpected errors
    throw error
  }
}

// Good: try...catch...finally combination
const uploadFile = async (file: File): Promise<UploadResult> => {
  setUploading(true)
  try {
    const result = await fileService.upload(file)
    showSuccessMessage('File uploaded successfully')
    return result
  } catch (error) {
    if (error instanceof FileTooLargeError) {
      showErrorMessage('File is too large. Maximum size is 10MB.')
    } else {
      showErrorMessage('Upload failed. Please try again.')
    }
    throw error
  } finally {
    setUploading(false)
  }
}
```

### 5.8 Logical Assignment Operators

Use logical assignment operators for concise conditional assignments.

Reference: [MDN - Logical AND assignment](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Logical_AND_assignment)

```typescript
// Good: Nullish coalescing assignment
let config = getUserConfig()
config.theme ??= 'light'  // Assign if null/undefined
config.pageSize ??= 30

// Good: Logical OR assignment (for all falsy values)
let errorMessage = ''
errorMessage ||= 'An unknown error occurred'

// Good: Logical AND assignment
let user = getUser()
user &&= normalizeUser(user)  // Transform only if truthy
```

---

## 6. API Communication Conventions

### 6.1 Type Naming for API

Follow consistent naming patterns for API-related types.

```typescript
// Request with query parameters: suffix with RequestParams
interface UserSearchRequestParams {
  keyword: string
  page: number
  size: number
  sortField?: string
  sortOrder?: 'asc' | 'desc'
}

// Request with body (POST/PUT): suffix with RequestBody
interface CreateUserRequestBody {
  email: string
  name: string
  role: UserRole
  departmentId?: string
}

interface UpdateUserRequestBody {
  name?: string
  email?: string
  role?: UserRole
}

// Response data: suffix with ServerData
interface UserServerData {
  userId: string
  email: string
  name: string
  role: UserRole
  createdAt: string
  updatedAt: string
}

// For list responses, use array type
type UserListServerData = UserServerData[]

// Paginated response
interface PaginatedResponse<T> {
  items: T[]
  page: number
  size: number
  totalPage: number
  totalCount: number
}

type UserListResponse = PaginatedResponse<UserServerData>
```

### 6.2 API Function Naming

Use different naming conventions for API layer functions vs. service/component layer functions.

```typescript
// In /api folder: HTTP verb prefix (get, post, put, delete)
// api/users.ts
export const getUsers = (params: UserSearchRequestParams) => {
  return http.get<UserListResponse>('/users', { params })
}

export const getUserById = (userId: string) => {
  return http.get<UserServerData>(`/users/${userId}`)
}

export const postUser = (body: CreateUserRequestBody) => {
  return http.post<UserServerData>('/users', body)
}

export const putUser = (userId: string, body: UpdateUserRequestBody) => {
  return http.put<UserServerData>(`/users/${userId}`, body)
}

export const deleteUser = (userId: string) => {
  return http.delete(`/users/${userId}`)
}

// In services/components: action verb prefix (fetch, create, update, remove)
// services/userService.ts
export const fetchUsers = async (params: UserSearchRequestParams) => {
  const response = await getUsers(params)
  return response.data
}

export const fetchUserById = async (userId: string) => {
  const response = await getUserById(userId)
  return response.data
}

export const createUser = async (data: CreateUserRequestBody) => {
  const response = await postUser(data)
  return response.data
}

export const updateUser = async (userId: string, data: UpdateUserRequestBody) => {
  const response = await putUser(userId, data)
  return response.data
}

export const removeUser = async (userId: string) => {
  await deleteUser(userId)
}
```

---

## 7. Testing Guidelines

### 7.1 Given-When-Then Pattern

Structure all tests using the Given-When-Then pattern for clarity and consistency.

```typescript
import { describe, test, expect } from 'vitest'

describe('calculateDiscount', () => {
  test('should return discounted price when valid discount rate is provided', () => {
    // Given: Original price is 10000, discount rate is 10%
    const originalPrice = 10000
    const discountRate = 10

    // When: Calculate discount
    const result = calculateDiscount(originalPrice, discountRate)

    // Then: Should return 9000
    expect(result).toBe(9000)
  })

  test('should return original price when discount rate is 0', () => {
    // Given: Price with no discount
    const originalPrice = 10000
    const discountRate = 0

    // When: Calculate with zero discount
    const result = calculateDiscount(originalPrice, discountRate)

    // Then: Original price is returned
    expect(result).toBe(10000)
  })

  test('should return 0 when discount rate is 100%', () => {
    // Given: Full discount scenario
    const originalPrice = 10000
    const discountRate = 100

    // When: Apply full discount
    const result = calculateDiscount(originalPrice, discountRate)

    // Then: Price becomes 0
    expect(result).toBe(0)
  })

  test('should throw error when discount rate is negative', () => {
    // Given: Invalid negative discount rate
    const originalPrice = 10000
    const discountRate = -10

    // When & Then: Should throw validation error
    expect(() => calculateDiscount(originalPrice, discountRate))
      .toThrow('Discount rate must be between 0 and 100')
  })

  test('should throw error when discount rate exceeds 100', () => {
    // Given: Invalid discount rate over 100%
    const originalPrice = 10000
    const discountRate = 150

    // When & Then: Should throw validation error
    expect(() => calculateDiscount(originalPrice, discountRate))
      .toThrow('Discount rate must be between 0 and 100')
  })

  test('should handle decimal discount rates correctly', () => {
    // Given: Decimal discount rate
    const originalPrice = 10000
    const discountRate = 15.5

    // When: Calculate with decimal rate
    const result = calculateDiscount(originalPrice, discountRate)

    // Then: Correct discounted price
    expect(result).toBe(8450)
  })
})
```

### 7.2 Test Organization

Organize tests using nested `describe` blocks by feature and method.

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    test('should create user with valid data', () => {
      // Given: Valid user data
      const userData = {
        email: 'test@example.com',
        name: 'John Doe',
        role: UserRole.MEMBER,
      }

      // When: Create user
      const result = createUser(userData)

      // Then: User is created with generated ID
      expect(result).toMatchObject({
        email: 'test@example.com',
        name: 'John Doe',
        role: UserRole.MEMBER,
      })
      expect(result.id).toBeDefined()
    })

    test('should throw error when email is invalid', () => {
      // Given: Invalid email format
      const userData = {
        email: 'invalid-email',
        name: 'John Doe',
        role: UserRole.MEMBER,
      }

      // When & Then: Should throw validation error
      expect(() => createUser(userData))
        .toThrow('Invalid email format')
    })

    test('should throw error when name is empty', () => {
      // Given: Empty name
      const userData = {
        email: 'test@example.com',
        name: '',
        role: UserRole.MEMBER,
      }

      // When & Then: Should throw validation error
      expect(() => createUser(userData))
        .toThrow('Name is required')
    })
  })

  describe('updateUser', () => {
    test('should update existing user fields', () => {
      // Given: Existing user and update data
      const userId = 'user-123'
      const updateData = { name: 'Jane Doe' }

      // When: Update user
      const result = updateUser(userId, updateData)

      // Then: Only specified fields are updated
      expect(result.name).toBe('Jane Doe')
      expect(result.id).toBe(userId)
    })

    test('should throw error when user not found', () => {
      // Given: Non-existent user ID
      const userId = 'non-existent-id'
      const updateData = { name: 'Jane Doe' }

      // When & Then: Should throw not found error
      expect(() => updateUser(userId, updateData))
        .toThrow('User not found')
    })
  })

  describe('deleteUser', () => {
    test('should delete existing user', () => {
      // Given: Existing user
      const userId = 'user-123'

      // When: Delete user
      deleteUser(userId)

      // Then: User no longer exists
      expect(() => getUserById(userId))
        .toThrow('User not found')
    })
  })
})
```

### 7.3 Testing Best Practices

| Practice | Description |
|----------|-------------|
| Descriptive test names | Test names should describe the scenario in plain language |
| Boundary value tests | Always test edge cases: 0, empty string, null, max values |
| Single concept per test | Test one behavior per test (multiple assertions for same concept is OK) |
| Test behavior, not implementation | Avoid testing internal implementation details |
| Arrange-Act-Assert | Keep Given-When-Then structure clear with blank lines |
| Independent tests | Each test should be able to run in isolation |

```typescript
// Good: Boundary value tests
describe('validateAge', () => {
  test('should return true for minimum valid age (0)', () => {
    expect(validateAge(0)).toBe(true)
  })

  test('should return true for maximum valid age (150)', () => {
    expect(validateAge(150)).toBe(true)
  })

  test('should return false for negative age', () => {
    expect(validateAge(-1)).toBe(false)
  })

  test('should return false for age exceeding maximum', () => {
    expect(validateAge(151)).toBe(false)
  })
})

// Good: Testing behavior, not implementation
describe('ShoppingCart', () => {
  test('should calculate correct total when items are added', () => {
    // Given
    const cart = new ShoppingCart()
    
    // When
    cart.addItem({ id: '1', price: 100, quantity: 2 })
    cart.addItem({ id: '2', price: 50, quantity: 1 })
    
    // Then: Test the observable behavior (total), not internal state
    expect(cart.getTotal()).toBe(250)
  })
})
```

---

## 8. File Structure and Modules

### 8.1 Barrel Files (index.ts)

Use barrel files to create single entry points for related modules.

```typescript
// utils/index.ts
export * from './formatNumber'
export * from './formatDate'
export * from './validators'
export * from './currency'

// types/index.ts
export * from './user'
export * from './product'
export * from './order'

// constants/index.ts
export * from './common'
export * from './enum/recordStatus'
export * from './enum/userRole'

// Usage: Clean imports from single entry point
import { formatNumber, formatDate, validateEmail } from '@/utils'
import { User, Product, Order } from '@/types'
import { RecordStatus, UserRole, MAX_RETRY_COUNT } from '@/constants'
```

### 8.2 Namespace Exports

For related utilities that should be grouped, use namespace-style exports.

```typescript
// utils/index.ts
export * as dateUtils from './date'
export * as currencyUtils from './currency'
export * as validatorUtils from './validators'

// Usage
import { dateUtils, currencyUtils } from '@/utils'

const formattedDate = dateUtils.format(new Date())
const formattedPrice = currencyUtils.formatKRW(10000)
```

### 8.3 File Naming Conventions

| File Type | Naming Convention | Example |
|-----------|-------------------|---------|
| Regular TypeScript files | camelCase | `formatNumber.ts`, `userService.ts` |
| Type definition files | camelCase with `.d.ts` | `user.d.ts`, `api.d.ts` |
| Test files | Original name + `.test.ts` | `formatNumber.test.ts` |
| Constant/Enum files | camelCase | `recordStatus.ts`, `userRole.ts` |

### 8.4 Directory Structure

```
src/
├── api/                    # API layer (HTTP functions)
│   ├── helper/
│   │   ├── users/
│   │   │   ├── list.ts
│   │   │   ├── detail.ts
│   │   │   └── index.ts
│   │   └── products/
│   └── instances/
│       └── index.ts        # Axios instance configuration
├── constants/
│   ├── common.ts
│   ├── enum/
│   │   ├── recordStatus.ts
│   │   └── userRole.ts
│   ├── select-option/
│   │   └── common.ts
│   └── index.ts
├── types/
│   ├── api/
│   │   ├── user.d.ts
│   │   └── product.d.ts
│   ├── common.d.ts
│   └── index.ts
├── utils/
│   ├── formatNumber.ts
│   ├── formatDate.ts
│   ├── validators/
│   │   ├── email.ts
│   │   └── password.ts
│   └── index.ts
└── __tests__/
    ├── utils/
    │   └── formatNumber.test.ts
    └── validators/
        └── email.test.ts
```

---

## 9. Documentation

### 9.1 JSDoc Comments

Add JSDoc comments to all exported functions, especially those with complex logic or non-obvious behavior.

```typescript
/**
 * Calculates the discounted price based on the original price and discount rate.
 *
 * @param originalPrice - The original price before discount (must be non-negative)
 * @param discountRate - The discount rate as a percentage (0-100)
 * @returns The final price after applying the discount
 * @throws {Error} When discount rate is negative or greater than 100
 *
 * @example
 * // Basic usage
 * const finalPrice = calculateDiscount(10000, 10)
 * console.log(finalPrice) // 9000
 *
 * @example
 * // With decimal discount rate
 * const finalPrice = calculateDiscount(10000, 15.5)
 * console.log(finalPrice) // 8450
 */
const calculateDiscount = (originalPrice: number, discountRate: number): number => {
  if (discountRate < 0 || discountRate > 100) {
    throw new Error('Discount rate must be between 0 and 100')
  }
  return originalPrice * (1 - discountRate / 100)
}

/**
 * Validates an email address format.
 *
 * @param email - The email address to validate
 * @returns True if the email format is valid, false otherwise
 *
 * @example
 * validateEmail('user@example.com') // true
 * validateEmail('invalid-email') // false
 */
const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Formats a number as Korean Won currency.
 *
 * @param amount - The amount to format
 * @param options - Formatting options
 * @param options.showSymbol - Whether to include the ₩ symbol (default: true)
 * @param options.decimals - Number of decimal places (default: 0)
 * @returns Formatted currency string
 *
 * @example
 * formatKRW(1000000) // '₩1,000,000'
 * formatKRW(1000000, { showSymbol: false }) // '1,000,000'
 */
interface FormatKRWOptions {
  showSymbol?: boolean
  decimals?: number
}

const formatKRW = (amount: number, options: FormatKRWOptions = {}): string => {
  const { showSymbol = true, decimals = 0 } = options
  const formatted = amount.toLocaleString('ko-KR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })
  return showSymbol ? `₩${formatted}` : formatted
}
```

### 9.2 Interface Documentation

Document complex interfaces with property descriptions.

```typescript
/**
 * Represents a user in the system.
 */
interface User {
  /** Unique identifier for the user */
  id: string
  
  /** User's email address (used for login) */
  email: string
  
  /** User's display name */
  displayName: string
  
  /** User's role determining permissions */
  role: UserRole
  
  /** ISO 8601 timestamp of account creation */
  createdAt: string
  
  /** ISO 8601 timestamp of last profile update */
  updatedAt: string
  
  /** Whether the user has verified their email */
  isEmailVerified: boolean
  
  /** Optional profile image URL */
  avatarUrl?: string
}

/**
 * Parameters for searching users.
 */
interface UserSearchParams {
  /** Search keyword (matches email or displayName) */
  keyword?: string
  
  /** Filter by user role */
  role?: UserRole
  
  /** Filter by email verification status */
  isEmailVerified?: boolean
  
  /** Page number (0-indexed) */
  page: number
  
  /** Number of items per page (max: 100) */
  size: number
  
  /** Field to sort by */
  sortField?: 'createdAt' | 'displayName' | 'email'
  
  /** Sort direction */
  sortOrder?: 'asc' | 'desc'
}
```

### 9.3 When to Document

| Scenario | Document? | Notes |
|----------|-----------|-------|
| Public/exported functions | Yes | Always document exported functions |
| Complex algorithms | Yes | Explain the logic and any non-obvious behavior |
| Functions with side effects | Yes | Document what side effects occur |
| Simple getters/setters | No | Self-explanatory from naming |
| Private utility functions | Optional | Document if logic is non-obvious |
| Type/Interface properties | Yes | Document non-obvious properties |

---

## 10. Code Generation Checklist

Use this checklist before submitting code for review.

### Naming

- [ ] Variables use `camelCase`
- [ ] Constants use `SCREAMING_SNAKE_CASE`
- [ ] Arrays are suffixed with `List`
- [ ] Option arrays use `_OPTION_LIST` suffix with `{ label, value }` structure
- [ ] Event handlers follow `handle` + `Event` + `Subject` pattern
- [ ] Types/Interfaces use `PascalCase`
- [ ] No abbreviations in names (except well-known: `id`, `url`, `api`)

### TypeScript

- [ ] Type imports use `import type`
- [ ] Enums are used instead of `as const` objects
- [ ] Functions with 3+ parameters use interface
- [ ] Generic types have descriptive names (or single letter for simple patterns)
- [ ] Return types are explicitly declared
- [ ] Namespace is used to group related API types

### Syntax

- [ ] `??` is used for null/undefined checks (not `||`)
- [ ] `defaultTo` from lodash-es is used for Number defaults
- [ ] `===` strict equality is used everywhere
- [ ] `?.` optional chaining is used for safe property access
- [ ] `async/await` is used instead of Promise chains
- [ ] Early return pattern is applied to reduce nesting
- [ ] Ternary is only used for simple, single-line assignments

### Functions

- [ ] Arrow function expressions are used (not function declarations)
- [ ] Each function has single responsibility
- [ ] Maximum 2 direct parameters (use interface for more)
- [ ] Return types are explicitly declared
- [ ] JSDoc comments are added for exported functions

### Error Handling

- [ ] `try...finally` is used when interceptor handles catch
- [ ] `try...catch` is used for custom error handling
- [ ] Errors are re-thrown after handling when appropriate

### API Conventions

- [ ] Request params types end with `RequestParams`
- [ ] Request body types end with `RequestBody`
- [ ] Response types end with `ServerData`
- [ ] API functions use HTTP verb prefix (`get`, `post`, `put`, `delete`)
- [ ] Service functions use action verb prefix (`fetch`, `create`, `update`, `remove`)

### Testing

- [ ] Tests follow Given-When-Then pattern
- [ ] Test names describe scenarios clearly in plain language
- [ ] Boundary cases are covered (0, empty, null, max values)
- [ ] Tests are organized with nested `describe` blocks
- [ ] Each test is independent and can run in isolation

### Documentation

- [ ] JSDoc comments added to exported functions
- [ ] Complex interfaces have property descriptions
- [ ] Examples are provided for non-obvious usage

---

## References

- Based on FLO Frontend Projects
- [MDN Web Docs - JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
