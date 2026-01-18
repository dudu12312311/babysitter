# Requirements Document

## Introduction

本文档定义育儿模拟器数据库设计的需求规格。系统需要将现有的JSON文件存储迁移到Supabase（PostgreSQL），支持用户管理、孩子信息、父母状态、游戏状态、任务系统和用户行为记录等核心功能。

## Glossary

- **User**: 使用育儿模拟器的玩家用户
- **Child**: 用户创建的虚拟孩子实体
- **Child_State**: 孩子在某一时刻的状态快照（健康值、情绪值、发育值）
- **Baby_Stage**: 孩子的成长阶段（新生儿0-3月、婴儿4-12月、幼儿1-3岁、学龄前4-5岁）
- **Task**: 系统预设的育儿任务/事件
- **Response_Option**: 任务对应的用户可选回应选项
- **User_Choice**: 用户在任务中做出的选择记录
- **Game_Session**: 用户的一次完整游戏会话
- **Parent_State**: 父母在某一时刻的状态快照（精力值、压力值、技能熟练度）
- **Supabase**: 基于PostgreSQL的云数据库服务，提供实时订阅和认证功能

## Requirements

### Requirement 1: 用户管理

**User Story:** As a 玩家, I want to 创建和管理我的账户, so that 我可以保存游戏进度并关联我的虚拟孩子。

#### Acceptance Criteria

1. THE Database SHALL store user information including unique identifier, gender, schedule preferences, difficulty level, and parenting goals
2. WHEN a user registers, THE Database SHALL generate a unique user_id and record creation timestamp
3. THE Database SHALL support storing user schedule as work_time and sleep_time fields
4. THE Database SHALL store difficulty level as an enumeration (beginner, standard, challenge)

### Requirement 2: 孩子信息管理

**User Story:** As a 玩家, I want to 创建和管理虚拟孩子信息, so that 我可以在游戏中照顾我的虚拟孩子。

#### Acceptance Criteria

1. THE Database SHALL store child information including name, gender, personality type, and AI-generated avatar URL
2. WHEN a child is created, THE Database SHALL associate it with exactly one user via foreign key
3. THE Database SHALL store personality as one of five predefined types
4. THE Database SHALL record child creation timestamp and last update timestamp
5. THE Database SHALL support storing the child's current stage (newborn, infant, toddler, preschooler)

### Requirement 3: 孩子状态追踪

**User Story:** As a 玩家, I want to 查看孩子的当前状态, so that 我可以了解孩子的健康值、情绪值和发育值。

#### Acceptance Criteria

1. THE Database SHALL store child state including health, mood, and development values as floating-point numbers between 0 and 100
2. WHEN child state changes, THE Database SHALL create a new state record with timestamp
3. THE Database SHALL maintain a history of all state changes for report generation
4. THE Database SHALL store the current stage in each state record
5. THE Database SHALL support querying the latest state for a given child

### Requirement 4: 任务系统

**User Story:** As a 系统管理员, I want to 配置阶段性任务和回应选项, so that 玩家可以在不同阶段面对相应的育儿挑战。

#### Acceptance Criteria

1. THE Database SHALL store tasks with stage association, task content, and category
2. THE Database SHALL store multiple response options for each task
3. WHEN storing a response option, THE Database SHALL include option text and impact values for health, mood, and development
4. THE Database SHALL support filtering tasks by baby stage
5. THE Database SHALL store task difficulty and estimated duration

### Requirement 5: 用户选择记录

**User Story:** As a 玩家, I want to 记录我在游戏中的所有选择, so that 系统可以生成我的育儿风格报告。

#### Acceptance Criteria

1. WHEN a user makes a choice, THE Database SHALL record the task, selected option, and response time
2. THE Database SHALL associate each choice record with a specific game session
3. THE Database SHALL store the resulting state changes after each choice
4. THE Database SHALL support querying all choices for a given session for report generation

### Requirement 6: 游戏会话管理

**User Story:** As a 玩家, I want to 管理我的游戏会话, so that 我可以暂停和继续游戏进度。

#### Acceptance Criteria

1. THE Database SHALL store game session with user, child, start time, and current progress
2. WHEN a session is created, THE Database SHALL record the initial child state
3. THE Database SHALL support session status (active, paused, completed)
4. WHEN a session completes, THE Database SHALL record end time and final statistics
5. THE Database SHALL support querying active sessions for a user

### Requirement 7: 父母状态追踪

**User Story:** As a 玩家, I want to 追踪我的父母角色状态, so that 我可以了解育儿对父母精力和压力的影响。

#### Acceptance Criteria

1. THE Database SHALL store parent state including energy, stress, and skill_level values as floating-point numbers between 0 and 100
2. WHEN parent state changes, THE Database SHALL create a new state record with timestamp
3. THE Database SHALL maintain a history of all parent state changes for report generation
4. THE Database SHALL associate parent state with the corresponding game session
5. THE Database SHALL support querying the latest parent state for a given session

### Requirement 8: 数据完整性

**User Story:** As a 系统, I want to 确保数据完整性, so that 所有关联数据保持一致。

#### Acceptance Criteria

1. THE Database SHALL enforce foreign key constraints between related tables
2. WHEN a user is deleted, THE Database SHALL cascade delete all associated children, sessions, and records
3. THE Database SHALL enforce value constraints (health, mood, development, energy, stress between 0-100)
4. THE Database SHALL use appropriate indexes for frequently queried fields
5. IF an invalid foreign key reference is attempted, THEN THE Database SHALL reject the operation

### Requirement 9: 报告数据支持

**User Story:** As a 玩家, I want to 获取成长档案和育儿风格报告, so that 我可以了解我的育儿表现。

#### Acceptance Criteria

1. THE Database SHALL support efficient queries for aggregating state history data
2. THE Database SHALL support calculating average, min, max values for health, mood, development, energy, and stress
3. THE Database SHALL support querying total response time and choice count per session
4. THE Database SHALL store computed report data for caching purposes

### Requirement 10: Supabase部署

**User Story:** As a 开发者, I want to 将数据库部署到Supabase, so that 应用可以使用云端PostgreSQL数据库。

#### Acceptance Criteria

1. THE System SHALL connect to Supabase PostgreSQL using connection string from environment variables
2. THE System SHALL use Supabase client library for database operations
3. THE Database SHALL support Row Level Security (RLS) policies for data isolation
4. THE System SHALL handle Supabase connection pooling appropriately
5. THE System SHALL support both direct connection and pooled connection modes
